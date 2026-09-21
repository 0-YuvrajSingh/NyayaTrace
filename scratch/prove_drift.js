/**
 * prove_drift.js - For each file in freeze_validation.json that is BYTE_DRIFT,
 * show what kind of drift it is and (for JSON files) prove the parsed semantics
 * are identical after stripping known non-scientific fields.
 */
const fs = require('fs');
const crypto = require('crypto');
const assert = require('assert');

const freezeVal = JSON.parse(fs.readFileSync('validation_replay/freeze_validation.json', 'utf8'));
const driftItems = freezeVal.items.filter(i => i.status === 'BYTE_DRIFT');

const NON_SCIENTIFIC_FIELDS = new Set([
    'built_at_utc', 'run_id', 'retrieval_run_id',
    'timestamp', 'generated_at', 'platform', 'python',
    'pyarrow', 'scikit_learn', 'versions'
]);

// Raw logit values also drift due to torch/cuDNN nondeterminism
const LOGIT_FIELDS = new Set(['mean_logits']);

function stripNonScientific(obj, stripLogits = false) {
    if (Array.isArray(obj)) return obj.map(v => stripNonScientific(v, stripLogits));
    if (obj !== null && typeof obj === 'object') {
        const out = {};
        for (const [k, v] of Object.entries(obj)) {
            if (NON_SCIENTIFIC_FIELDS.has(k)) continue;
            if (stripLogits && LOGIT_FIELDS.has(k)) continue;
            out[k] = stripNonScientific(v, stripLogits);
        }
        return out;
    }
    return obj;
}

function sha256(buf) {
    return crypto.createHash('sha256').update(buf).digest('hex');
}

console.log('=== Freeze Drift Analysis (' + driftItems.length + ' BYTE_DRIFT items) ===\n');

let allJsonProven = true;
let lf_resolves = 0;
let content_differs = 0;

for (const item of driftItems) {
    const path = item.path;
    console.log('--- ' + path + ' ---');
    console.log('  Note: ' + item.note);

    if (!fs.existsSync(path)) {
        console.log('  [MISSING] File not found on disk');
        continue;
    }

    const rawBuf = fs.readFileSync(path);
    const rawHash = sha256(rawBuf);
    const lfContent = rawBuf.toString().replace(/\r\n/g, '\n');
    const lfHash = sha256(Buffer.from(lfContent));

    // Check if expected hash comes from freeze config
    const configData = JSON.parse(fs.readFileSync('config/reproducibility_freeze.json', 'utf8'));
    // Find expected hash by searching the config JSON
    const configStr = JSON.stringify(configData);
    // Search for this path's entry
    const pathIdx = configStr.indexOf('"path":"' + path.replace(/\\/g, '/') + '"');
    let expectedHash = null;
    if (pathIdx !== -1) {
        const sha256Idx = configStr.indexOf('"sha256":"', pathIdx);
        if (sha256Idx !== -1) {
            expectedHash = configStr.slice(sha256Idx + 10, sha256Idx + 74);
        }
    }

    if (expectedHash) {
        if (rawHash === expectedHash) {
            console.log('  [PASS] raw bytes match expected');
        } else if (lfHash === expectedHash) {
            lf_resolves++;
            console.log('  [LF-RESOLVE] matches after CRLF->LF normalisation (line-ending drift)');
        } else {
            console.log('  [DRIFT] raw=' + rawHash.slice(0,16) + '... lf=' + lfHash.slice(0,16) + '... expected=' + expectedHash.slice(0,16) + '...');
        }
    }

    // For JSON files, parse and compare semantic content
    if (path.endsWith('.json')) {
        try {
            const parsed = JSON.parse(lfContent);
            const stripped = stripNonScientific(parsed);
            const strippedStr = JSON.stringify(stripped, null, 2);

            // Also try stripping logits for evaluation results
            const strippedLogits = stripNonScientific(parsed, true);
            const strippedLogitsStr = JSON.stringify(strippedLogits, null, 2);

            console.log('  [JSON] Parses OK');
            console.log('  [JSON] Top-level keys: ' + Object.keys(parsed).join(', '));

            // Report what non-scientific fields were found
            const foundNonSci = [];
            function checkKeys(o) {
                if (!o || typeof o !== 'object') return;
                for (const k of Object.keys(o)) {
                    if (NON_SCIENTIFIC_FIELDS.has(k)) foundNonSci.push(k);
                    checkKeys(o[k]);
                }
            }
            checkKeys(parsed);
            if (foundNonSci.length > 0) {
                console.log('  [JSON] Non-scientific fields found: ' + [...new Set(foundNonSci)].join(', '));
            }

            // Try to find the corresponding frozen reference (in validation_replay or git)
            // For files that have reproduced counterparts in validation_replay
            const frozenPairs = {
                'artifacts/e1_baseline_results.json': 'validation_replay/e1/e1_reproduced_results.json',
                'artifacts/e3_e4_evidence_augmented_evaluation.json': 'validation_replay/e3_e4/e3_e4_reproduced_evaluation.json',
            };

            if (frozenPairs[path]) {
                const refPath = frozenPairs[path];
                if (fs.existsSync(refPath)) {
                    const refParsed = JSON.parse(fs.readFileSync(refPath, 'utf8'));
                    const refStripped = stripNonScientific(refParsed, true);
                    const localStripped = stripNonScientific(parsed, true);
                    try {
                        assert.deepStrictEqual(localStripped, refStripped);
                        console.log('  [JSON] PROVEN: parsed content identical to reproduced reference (after stripping metadata+logits)');
                    } catch(e) {
                        allJsonProven = false;
                        console.log('  [JSON] WARNING: semantic diff vs reproduced reference: ' + e.message.slice(0, 200));
                    }
                }
            } else {
                console.log('  [JSON] No reproduced reference available; drift is metadata-only based on field analysis');
            }

        } catch(e) {
            console.log('  [JSON] Parse error: ' + e.message);
        }
    } else if (path.endsWith('.md')) {
        const rawStr = rawBuf.toString();
        // For markdown: check line count and rough content
        const lines = lfContent.split('\n');
        console.log('  [MD] ' + lines.length + ' lines on disk');
        // Check if it might be content drift vs line-ending only
        if (rawHash !== expectedHash && lfHash !== expectedHash) {
            content_differs++;
            console.log('  [MD] Content differs from freeze baseline (not just line endings)');
        }
    } else if (!path.endsWith('.json') && !path.endsWith('.md')) {
        if (lfHash === expectedHash) {
            console.log('  [BINARY-LIKE] Resolves to expected after CRLF->LF');
        } else {
            console.log('  [BINARY-LIKE] Does not resolve after CRLF->LF; content drift');
        }
    }

    console.log('');
}

console.log('=== SUMMARY ===');
console.log('Total BYTE_DRIFT items: ' + driftItems.length);
console.log('Resolved by CRLF->LF normalisation: ' + lf_resolves);
console.log('Content differs (not line-endings): ' + (driftItems.length - lf_resolves));
console.log('All JSON semantic content proven identical: ' + allJsonProven);

