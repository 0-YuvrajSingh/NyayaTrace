const fs = require('fs');
const path = require('path');

const targets = ['submission', 'docs', 'experiments', 'answer_key', 'artifacts', 'scripts'];

function walk(dir) {
  let results = [];
  try {
    const list = fs.readdirSync(dir, { withFileTypes: true });
    for (const ent of list) {
      const full = path.join(dir, ent.name);
      if (ent.isDirectory()) {
        results.push(...walk(full));
      } else if (ent.isFile() && /\.(json|md|py|tex|txt)$/.test(ent.name)) {
        try {
          const content = fs.readFileSync(full, 'utf8');
          if (content.includes('0.6486') || content.includes('0.6073') || content.includes('Combined-37')) {
            console.log(`Found in ${full}`);
          }
        } catch (e) {}
      }
    }
  } catch (e) {}
  return results;
}

targets.forEach(t => walk(t));

