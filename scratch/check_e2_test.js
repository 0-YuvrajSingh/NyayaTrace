const fs = require('fs');
const d = JSON.parse(fs.readFileSync('artifacts/e2_chunk_pool_results.json', 'utf8'));
console.log('E2 test results:', d.test_results);

