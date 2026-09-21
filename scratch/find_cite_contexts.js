const fs = require('fs');
const tex = fs.readFileSync('submission/final/paper_master.tex', 'utf8');
const lines = tex.split(/\r?\n/);

const bibItems = [
  'malik2021', 'paul2023', 'taxflow2026', 'casefacts2026', 'lextime2025',
  'poojasingh2026', 'robertson2009', 'smith2007', 'coliee2023', 'legalbench2023',
  'casehold2021', 'shukla2022', 'dahl2024', 'nay2023', 'lewis2020'
];

bibItems.forEach((b, idx) => {
  console.log(`\n================== [${idx+1}] ${b} ==================`);
  lines.forEach((l, i) => {
    if (l.includes(b)) {
      console.log(`L${i+1}: ${l.trim()}`);
    }
  });
});

