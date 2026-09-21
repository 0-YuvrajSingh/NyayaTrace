const fs = require('fs');
const tex = fs.readFileSync('submission/final/paper_master.tex', 'utf8');

// Find all \cite occurrences in the body (before \begin{thebibliography})
const bibStart = tex.indexOf('\\begin{thebibliography}');
const body = tex.slice(0, bibStart);

const citeRegex = /\\cite\{([^}]+)\}/g;
let m;
const orderOfFirstUse = [];
const seenCites = new Set();

while ((m = citeRegex.exec(body)) !== null) {
  const keys = m[1].split(',').map(s => s.trim());
  for (const k of keys) {
    if (!seenCites.has(k)) {
      seenCites.add(k);
      orderOfFirstUse.push(k);
    }
  }
}

// Find all \bibitem entries
const bibRegex = /\\bibitem\{([^}]+)\}/g;
const bibItems = [];
while ((m = bibRegex.exec(tex)) !== null) {
  bibItems.push(m[1].trim());
}

console.log('Total bibitems in bibliography:', bibItems.length);
console.log('Total unique keys cited in body:', seenCites.size);

console.log('\nOrder of first use in text:');
orderOfFirstUse.forEach((k, idx) => console.log(`  [${idx+1}] ${k}`));

console.log('\nOrder of bibitems in bibliography:');
bibItems.forEach((k, idx) => console.log(`  [${idx+1}] ${k}`));

let orderMatches = true;
for (let i = 0; i < Math.max(bibItems.length, orderOfFirstUse.length); i++) {
  if (bibItems[i] !== orderOfFirstUse[i]) {
    console.log(`MISMATCH at index ${i+1}: text has '${orderOfFirstUse[i]}', bibitem has '${bibItems[i]}'`);
    orderMatches = false;
  }
}
console.log('\nDoes bibliography order match order of first use perfectly?', orderMatches);

for (const k of seenCites) {
  if (!bibItems.includes(k)) {
    console.log('CITED BUT NOT IN BIBLIOGRAPHY:', k);
  }
}
for (const b of bibItems) {
  if (!seenCites.has(b)) {
    console.log('IN BIBLIOGRAPHY BUT NEVER CITED:', b);
  }
}
