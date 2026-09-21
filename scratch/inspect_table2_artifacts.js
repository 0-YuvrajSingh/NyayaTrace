const fs = require('fs');

function checkFile(p) {
  if (fs.existsSync(p)) {
    console.log(`=== ${p} ===`);
    const data = JSON.parse(fs.readFileSync(p, 'utf8'));
    console.log(JSON.stringify(data, null, 2).slice(0, 1000));
  } else {
    console.log(`Missing: ${p}`);
  }
}

checkFile('artifacts/e1_baseline_results.json');
checkFile('artifacts/e1_e2_comparison.json');
checkFile('artifacts/e3_e4_evidence_augmented_evaluation.json');
checkFile('artifacts/e2_chunk_pool_results.json');

