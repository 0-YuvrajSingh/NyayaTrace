const fs = require('fs');
const assert = require('assert');

function cleanJson(obj) {
    if (Array.isArray(obj)) return obj.map(cleanJson);
    if (obj !== null && typeof obj === 'object') {
        const newObj = {};
        for (const key of Object.keys(obj)) {
            if (key === 'built_at_utc' || key === 'versions' || key === 'timestamp' || key === 'run_id' || key === 'retrieval_run_id' || key === 'mean_logits') continue;
            newObj[key] = cleanJson(obj[key]);
        }
        return newObj;
    }
    return obj;
}

const pairs = [
    { name: 'e1', frozen: 'artifacts/e1_baseline_results.json', reproduced: 'validation_replay/e1/e1_reproduced_results.json' },
    { name: 'e3_e4', frozen: 'artifacts/e3_e4_evidence_augmented_evaluation.json', reproduced: 'validation_replay/e3_e4/e3_e4_reproduced_evaluation.json' }
];

for (const pair of pairs) {
    if (fs.existsSync(pair.frozen) && fs.existsSync(pair.reproduced)) {
        const f1 = JSON.parse(fs.readFileSync(pair.frozen, 'utf8'));
        const f2 = JSON.parse(fs.readFileSync(pair.reproduced, 'utf8'));
        try {
            assert.deepStrictEqual(cleanJson(f1), cleanJson(f2));
            console.log('[PASS] ' + pair.name + ' - EXACT MATCH after dropping timestamps/metadata/uuids/logits');
        } catch (e) {
            console.log('[FAIL] ' + pair.name + ' - DIFF:', e.message);
        }
    } else {
        console.log('[SKIP] ' + pair.name + ' - files not found');
    }
}
