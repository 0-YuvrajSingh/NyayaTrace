const fs = require('fs');
const crypto = require('crypto');
const path = require('path');

function sha256(filePath) {
  const fileBuffer = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(fileBuffer).digest('hex');
}

console.log('=== Checking files in submission/final/ ===');
const finalDir = 'submission/final';
const files = fs.readdirSync(finalDir);

const hashes = {};
files.forEach(f => {
  const full = path.join(finalDir, f);
  if (fs.statSync(full).isFile()) {
    hashes[f] = sha256(full);
    console.log(`${f.padEnd(35)} : ${hashes[f]}`);
  }
});

console.log('\n=== Checking figures/ in submission/final/figures/ ===');
const figDir = 'submission/final/figures';
if (fs.existsSync(figDir)) {
  fs.readdirSync(figDir).forEach(f => {
    const full = path.join(figDir, f);
    if (fs.statSync(full).isFile()) {
      const h = sha256(full);
      console.log(`figures/${f.padEnd(27)} : ${h}`);
    }
  });
}

console.log('\n=== Reading MANIFEST.md in submission/final/ ===');
const manifestPath = 'submission/final/MANIFEST.md';
if (fs.existsSync(manifestPath)) {
  const manifest = fs.readFileSync(manifestPath, 'utf8');
  console.log(manifest);
} else {
  console.log('MANIFEST.md missing!');
}

