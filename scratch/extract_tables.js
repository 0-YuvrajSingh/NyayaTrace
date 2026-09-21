const fs = require('fs');
const text = fs.readFileSync('submission/final/paper_master.tex', 'utf8');
const lines = text.split(/\r?\n/);
lines.forEach((line, idx) => {
  if (line.includes('\\begin{table')) {
    console.log(`\n=== Table at line ${idx+1} ===`);
    let j = idx;
    while (j < lines.length && !lines[j].includes('\\end{table')) {
      console.log(lines[j]);
      j++;
    }
    if (j < lines.length) console.log(lines[j]);
  }
});

