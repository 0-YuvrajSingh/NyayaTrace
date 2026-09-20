const fs = require('fs');

function cleanJson(obj) {
    if (Array.isArray(obj)) return obj.map(cleanJson);
    if (obj !== null && typeof obj === 'object') {
        const newObj = {};
        for (const key of Object.keys(obj)) {
            if (key === 'built_at_utc' || key === 'versions' || key === 'timestamp' || key === 'run_id') continue;
            newObj[key] = cleanJson(obj[key]);
        }
        return newObj;
    }
    return obj;
}

const f1 = JSON.parse(fs.readFileSync('artifacts/e1_baseline_results.json', 'utf8'));
const f2 = JSON.parse(fs.readFileSync('validation_replay/e1/e1_reproduced_results.json', 'utf8'));

const assert = require('assert');
try {
    assert.deepStrictEqual(cleanJson(f1), cleanJson(f2));
    console.log('e1 EXACT MATCH after cleaning');
} catch (e) {
    console.log('e1 DIFF:', e.message);
}
