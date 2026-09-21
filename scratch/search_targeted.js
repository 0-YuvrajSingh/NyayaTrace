const fs = require('fs');
const path = require('path');

const dirs = ['artifacts', 'answer_key', 'docs', 'experiments', 'scripts', 'validation_prep', 'validation_replay', 'submission'];

function searchDir(dir, pattern) {
  const results = [];
  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const ent of entries) {
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
  } catch (e) {}
  return results;
}

dirs.forEach(d => {
  const r1 = searchDir(d, 'Extension-7');
  if (r1.length > 0) console.log(`Extension-7 in ${d}:`, r1);
  const r2 = searchDir(d, 'Combined-37');
  if (r2.length > 0) console.log(`Combined-37 in ${d}:`, r2);
  const r3 = searchDir(d, '0.6015');
  if (r3.length > 0) console.log(`0.6015 in ${d}:`, r3);
});

