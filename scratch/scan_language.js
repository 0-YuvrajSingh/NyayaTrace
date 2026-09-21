const fs = require('fs');
const tex = fs.readFileSync('submission/final/paper_master.tex', 'utf8');
const lines = tex.split(/\r?\n/);

const patterns = [
  /caus(e|al|ing|ed)/i,
  /guarantee/i,
  /ensur(e|es|ed|ing)/i,
  /prov(e|es|ed|en)\b/i,
  /superior/i,
  /significan/i,
  /without regressing/i,
  /raised\b/i,
  /eliminat/i,
  /dramatic/i
];

patterns.forEach(pat => {
  console.log(`\n=== Matches for ${pat} ===`);
  lines.forEach((l, idx) => {
    if (pat.test(l)) {
      console.log(`${idx+1}: ${l.trim()}`);
    }
  });
});

