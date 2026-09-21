const fs = require('fs');
const crypto = require('crypto');

const freezeConfig = JSON.parse(fs.readFileSync('config/reproducibility_freeze.json', 'utf8'));

// The 10 differing files
const differingFiles = [
  'corpus/dataset_manifest.md',
  'artifacts/ecourts_corpus_identity.json',
  'artifacts/bm25_index.json',
  'artifacts/e1_baseline_results.json',
  'artifacts/e2_correction_manifest.json',
  'artifacts/e3_e4_evidence_augmented_evaluation.json',
  'artifacts/e3_e4_prediction_error_analysis.json',
  'artifacts/week10_post_selfmatch_freeze_regression.json',
  'artifacts/week10_dev_probe_selfmatch_recheck.json',
  'artifacts/week11_temporal_prerank_evaluation.json'
];

for (const path of differingFiles) {
  console.log(`=======================================================`);
  console.log(`PATH: ${path}`);
  const raw = fs.readFileSync(path);
  const currentSha = crypto.createHash('sha256').update(raw).digest('hex');
  console.log(`Current SHA-256: ${currentSha}`);
  
  if (path.endsWith('.json')) {
    const data = JSON.parse(raw.toString('utf8'));
    console.log(`Top-level keys: ${Object.keys(data).join(', ')}`);
    
    // Check for volatile fields
    const volatileFound = {};
    function scan(obj, prefix='') {
      if (!obj || typeof obj !== 'object') return;
      for (const [k, v] of Object.entries(obj)) {
        const fullKey = prefix ? `${prefix}.${k}` : k;
        if (['built_at_utc', 'timestamp', 'generated_at', 'run_id', 'retrieval_run_id', 'versions'].includes(k)) {
          volatileFound[fullKey] = v;
        } else if (typeof v === 'object') {
          scan(v, fullKey);
        }
      }
    }
    scan(data);
    console.log('Volatile fields found:');
    for (const [k, v] of Object.entries(volatileFound)) {
      console.log(`  ${k}: ${JSON.stringify(v).slice(0, 100)}`);
    }
  } else {
    // markdown
    const lines = raw.toString('utf8').split('\n');
    console.log(`Markdown lines: ${lines.length}, bytes: ${raw.length}`);
    console.log(`Header lines:\n${lines.slice(0, 10).join('\n')}`);
  }
}

