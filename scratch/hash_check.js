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

let total = 0;
let exact = 0;
let drift = 0;
let missing = 0;

async function checkHashes() {
    console.log('Total unique paths with expected hashes: ' + Object.keys(expectedHashes).length);
    for (const [path, expectedSha] of Object.entries(expectedHashes)) {
        total++;
        if (!fs.existsSync(path)) {
            missing++;
            console.log('[MISSING] ' + path);
            continue;
        }
        
        const hash = await new Promise((resolve, reject) => {
            const h = crypto.createHash('sha256');
            const stream = fs.createReadStream(path);
            stream.on('data', chunk => h.update(chunk));
            stream.on('end', () => resolve(h.digest('hex')));
            stream.on('error', reject);
        });

        if (hash === expectedSha) {
            exact++;
        } else {
            drift++;
            console.log('[DRIFT] ' + path + ' (Expected: ' + expectedSha + ', Got: ' + hash + ')');
        }
    }
    console.log('\nResults:');
    console.log('Total: ' + total);
    console.log('Exact: ' + exact);
    console.log('Drift: ' + drift);
    console.log('Missing: ' + missing);
}
checkHashes();
