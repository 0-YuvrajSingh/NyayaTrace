const AdmZip = require('adm-zip');
const fs = require('fs');
const crypto = require('crypto');

const zipPath = 'submission/final/nyayatrace_submission_package.zip';
if (!fs.existsSync(zipPath)) {
  console.log('Zip does not exist');
  process.exit(1);
}

// Check if adm-zip is installed or use node built-in / python in docker
console.log('Zip file exists, size:', fs.statSync(zipPath).size);

