const fs = require('fs');
const path = require('path');

function searchDir(dir, pattern) {
  const results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const ent of entries) {
    if (ent.name === '.git' || ent.name === 'node_modules') continue;
    const fullPath = path.join(dir, ent.name);
    if (ent.isDirectory()) {
      results.push(...searchDir(fullPath, pattern));
    } else if (ent.isFile()) {
      try {
        const text = fs.readFileSync(fullPath, 'utf8');
        if (text.includes(pattern)) {
          results.push(fullPath);
        }
      } catch (e) {}
    }
  }
  return results;
}

console.log('Search for 0.3243:');
console.log(searchDir('.', '0.3243'));

console.log('\nSearch for Extension-7:');
console.log(searchDir('.', 'Extension-7'));

console.log('\nSearch for Combined-37:');
console.log(searchDir('.', 'Combined-37'));

console.log('\nSearch for 0.6015:');
console.log(searchDir('.', '0.6015'));

