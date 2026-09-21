const fs = require('fs');
const crypto = require('crypto');
const { execSync } = require('child_process');

const targetHashes = {
  'corpus/dataset_manifest.md': 'e57fa817b1ed351cfb98f7e10332e35429371388187276366b04126a15ae31f1',
  'artifacts/ecourts_corpus_identity.json': 'd88d6b197d6991efc44cfb2338618d4993473b524a123cab9bb4d35e785d77ca',
  'artifacts/bm25_index.json': '6e904436c515aa34ed9ea09214f32969e2e48bf5e3a495d1b8e0a674eb8aded8',
  'artifacts/e1_baseline_results.json': '0726043d7e2445886f7c8658e4c7b8560f321d079b3e8203aa2d5890c9ccf13d',
  'artifacts/e2_correction_manifest.json': '1ae92bc5e5b54fac129480e3c647dd755527cd66fc8f4fa476c636c4341b9f0e',
  'artifacts/e3_e4_evidence_augmented_evaluation.json': 'e28ea37e67e5d2b4a3d35e448bddba14b35573ed170f0726c394dc2aa0a16270',
  'artifacts/e3_e4_prediction_error_analysis.json': 'dbd2178aeadf14838484652972466d926170852a889e60a9465cf8a7883350bf',
  'artifacts/week10_post_selfmatch_freeze_regression.json': '84357553e57767899f2fea2054b7b348f940e46eb91b50a28d512e4898a2e317',
  'artifacts/week10_dev_probe_selfmatch_recheck.json': 'ffb92f8b3992de060f035d625eddb6e1c7ce2e02e1140fc57d73bf5cac57c0ec',
  'artifacts/week11_temporal_prerank_evaluation.json': '9a475febf1e0256deb3ace54d6257fab92985e94c165fd921e0bdec7b86a227d'
};

const commits = execSync('git rev-list --all').toString().trim().split(/\s+/);
console.log('Total commits to inspect:', commits.length);

for (const [path, expected] of Object.entries(targetHashes)) {
  console.log(`=== ${path} ===`);
  console.log(`  expected: ${expected}`);
  let matched = false;
  const seen = new Set();
  
  for (const c of commits) {
    try {
      const content = execSync(`git show ${c}:"${path}"`, { maxBuffer: 20*1024*1024 });
      const rawSha = crypto.createHash('sha256').update(content).digest('hex');
      const lfContent = Buffer.from(content.toString().replace(/\r\n/g, '\n'));
      const lfSha = crypto.createHash('sha256').update(lfContent).digest('hex');
      
      const sig = `${rawSha.slice(0, 16)}|${lfSha.slice(0, 16)}`;
      if (!seen.has(sig)) {
        seen.add(sig);
        console.log(`  commit ${c.slice(0,7)}: raw=${rawSha} lf=${lfSha}`);
      }
      if (rawSha === expected || lfSha === expected) {
        console.log(`  >>> FOUND MATCH in commit ${c.slice(0,7)}! (rawMatch=${rawSha===expected}, lfMatch=${lfSha===expected})`);
        matched = true;
      }
    } catch (e) {
      // not in this commit
    }
  }
  if (!matched) {
    console.log('  >>> NO MATCH found in any commit in local git history');
  }
}

