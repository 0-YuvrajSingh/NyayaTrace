const fs = require('fs');
const txt = fs.readFileSync('scratch/pdf_text.txt', 'utf8');
console.log('Total characters in extracted PDF text:', txt.length);
console.log('Contains "freeze audit":', txt.includes('freeze audit'));
console.log('Contains "validity filtering to Indian tax-law":', txt.includes('validity filtering to Indian tax-law'));
console.log('Contains "28 byte-exact, 1 after line":', txt.includes('28 byte-exact, 1 after line'));
console.log('Contains "per-file evidence in the repository audit":', txt.includes('per-file evidence in the repository audit'));
