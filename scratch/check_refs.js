const fs = require('fs');
const tex = fs.readFileSync('submission/final/paper_master.tex', 'utf8');

const labelRegex = /\\label\{([^}]+)\}/g;
const labels = {};
let m;
while ((m = labelRegex.exec(tex)) !== null) {
  labels[m[1]] = true;
}

const refRegex = /(Section|Table|Fig\.|Figure)\s*~?\\ref\{([^}]+)\}/gi;
let allResolved = true;
while ((m = refRegex.exec(tex)) !== null) {
  const type = m[1];
  const refKey = m[2];
  const exists = labels[refKey];
  console.log(`${type} ~\\ref{${refKey}} -> ${exists ? 'RESOLVED' : 'UNDEFINED'}`);
  if (!exists) allResolved = false;
}

console.log('\nAll float and section refs resolved:', allResolved);
