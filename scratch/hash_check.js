const fs = require('fs');
const crypto = require('crypto');

const config = JSON.parse(fs.readFileSync('config/reproducibility_freeze.json', 'utf8'));

const expectedHashes = {};
function extractHashes(obj) {
    if (!obj) return;
    if (typeof obj === 'object') {
        if (obj.path && obj.sha256) {
            expectedHashes[obj.path] = obj.sha256;
        }
        for (let key in obj) extractHashes(obj[key]);
    }
}
extractHashes(config);

const results = { exact: [], lf_resolve: [], content_drift: [], missing: [] };

async function streamHash(path) {
    return new Promise((resolve, reject) => {
        const h = crypto.createHash('sha256');
        const stream = fs.createReadStream(path);
        stream.on('data', chunk => h.update(chunk));
        stream.on('end', () => resolve(h.digest('hex')));
        stream.on('error', reject);
    });
}

async function checkHashes() {
    console.log('Total unique paths with expected hashes: ' + Object.keys(expectedHashes).length);
    for (const [path, expectedSha] of Object.entries(expectedHashes)) {
        if (!fs.existsSync(path)) {
            results.missing.push(path);
            console.log('[MISSING] ' + path);
            continue;
        }

        const rawHash = await streamHash(path);
        if (rawHash === expectedSha) {
            results.exact.push(path);
            continue;
        }

        // Try LF normalisation (only works on small text files)
        const stat = fs.statSync(path);
        if (stat.size < 10 * 1024 * 1024) { // < 10MB
            const raw = fs.readFileSync(path);
            const lfHash = crypto.createHash('sha256').update(Buffer.from(raw.toString().replace(/\r\n/g, '\n'))).digest('hex');
            if (lfHash === expectedSha) {
                results.lf_resolve.push(path);
                console.log('[LF-RESOLVE] ' + path);
                continue;
            }
        }

        results.content_drift.push(path);
        console.log('[CONTENT-DRIFT] ' + path + ' (Expected: ' + expectedSha.slice(0,16) + '..., Got: ' + rawHash.slice(0,16) + '...)');
    }

    console.log('\nResults:');
    console.log('Total: ' + (results.exact.length + results.lf_resolve.length + results.content_drift.length + results.missing.length));
    console.log('Raw exact:     ' + results.exact.length);
    console.log('LF-resolve:    ' + results.lf_resolve.length);
    console.log('Content drift: ' + results.content_drift.length);
    console.log('Missing:       ' + results.missing.length);
    console.log('\nLF-resolve files:', results.lf_resolve);
    console.log('\nContent drift files:', results.content_drift);
}
checkHashes();
