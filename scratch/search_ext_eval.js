const fs = require('fs');
const path = require('path');

const dirs = ['artifacts', 'experiments', 'scripts', 'docs', 'submission'];

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
  const r = searchDir(d, '0.6073');
  if (r.length > 0) console.log(`0.6073 in ${d}:`, r);
});

dirs.forEach(d => {
  const r = searchDir(d, 'verified_7_case_extension');
  if (r.length > 0) console.log(`verified_7_case_extension in ${d}:`, r);
});

