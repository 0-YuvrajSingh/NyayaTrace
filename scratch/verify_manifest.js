const fs = require('fs');
const crypto = require('crypto');

const manifest = fs.readFileSync('submission/final/MANIFEST.md', 'utf8');
const files = [
  'paper_master.pdf',
  'paper_master.tex',
  'nyayatrace_submission_package.zip',
  'figures/fig1_outcome.pdf',
  'figures/fig2_funnel.pdf',
  'figures/fig3_integrity.pdf',
  'figures/fig4_investigation.pdf',
  'figures/fig5_explanation.pdf'
];

let allMatch = true;
for (const f of files) {
  const hash = crypto.createHash('sha256').update(fs.readFileSync('submission/final/' + f)).digest('hex');
  const inManifest = manifest.includes(f) && manifest.includes(hash);
  console.log((inManifest ? '[MATCH] ' : '[FAIL] ') + f + ' : ' + hash);
  if (!inManifest) allMatch = false;
}
console.log('\nAll matched: ' + allMatch);

