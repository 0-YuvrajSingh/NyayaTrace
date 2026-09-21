const fs = require('fs');

const f1 = 'artifacts/week12_prediction_cross_reference.json';
if (fs.existsSync(f1)) {
  const d = JSON.parse(fs.readFileSync(f1, 'utf8'));
  console.log('week12_prediction_cross_reference:', JSON.stringify(d).slice(0, 500));
}

const f2 = 'artifacts/e3_e4_prediction_error_analysis.json';
if (fs.existsSync(f2)) {
  const d = JSON.parse(fs.readFileSync(f2, 'utf8'));
  console.log('e3_e4_prediction_error_analysis:', JSON.stringify(d).slice(0, 500));
}

