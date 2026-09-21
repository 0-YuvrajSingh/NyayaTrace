const fs = require('fs');
const path = require('path');

const artDir = 'artifacts';
const files = fs.readdirSync(artDir).filter(f => f.endsWith('.json'));

function searchArtifacts(term) {
  const matches = [];
  for (const f of files) {
    try {
      const content = fs.readFileSync(path.join(artDir, f), 'utf8');
      if (content.includes(term)) {
        matches.push(f);
      }
    } catch (e) {}
  }
  return matches;
}

const terms = [
  '0.61344',
  '0.612342',
  '0.596806',
  '0.592358',
  '0.6015',
  '0.5937',
  '0.666667',
  '0.603175',
  '0.324324',
  '0.540541',
  '0.648649',
  '0.607347',
  '0.7143',
  '0.5714',
  '1503',
  '684',
  '238',
  '213',
  '368',
  '1980_133',
  '2008_1629',
  '1985_40'
];

terms.forEach(t => {
  const m = searchArtifacts(t);
  console.log(`${t} -> in ${m.length} files: ${m.slice(0, 5).join(', ')}`);
});

