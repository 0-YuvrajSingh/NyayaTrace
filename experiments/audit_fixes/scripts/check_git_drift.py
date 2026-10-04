import subprocess, json

def main():
    drift_files = [
        "artifacts/bm25_index.json",
        "artifacts/e1_baseline_results.json",
        "artifacts/e2_correction_manifest.json",
        "artifacts/e3_e4_evidence_augmented_evaluation.json",
        "artifacts/e3_e4_prediction_error_analysis.json",
        "artifacts/ecourts_corpus_identity.json",
        "artifacts/week10_dev_probe_selfmatch_recheck.json",
        "artifacts/week10_post_selfmatch_freeze_regression.json",
        "artifacts/week11_temporal_prerank_evaluation.json",
        "corpus/dataset_manifest.md"
    ]
    with open('/repo/config/reproducibility_freeze.json') as f:
        data = json.load(f)
    paths_to_sha = {}
    def recurse(obj):
        if isinstance(obj, dict):
            if 'path' in obj and 'sha256' in obj: paths_to_sha[obj['path']] = obj['sha256']
            for v in obj.values(): recurse(v)
        elif isinstance(obj, list):
            for item in obj: recurse(item)
    recurse(data)
    
    import hashlib
    for f in drift_files:
        expected = paths_to_sha.get(f)
        commits = subprocess.check_output(['git', '-C', '/repo', 'log', '--format=%h', '--', f], text=True).split()
        found = False
        for c in commits:
            content = subprocess.check_output(['git', '-C', '/repo', 'show', f"{c}:{f}"])
            h = hashlib.sha256(content).hexdigest()
            hlf = hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest()
            if h == expected or hlf == expected:
                found = True
                print(f"{f}: found in commit {c}")
                break
        if not found:
            print(f"{f}: expected {expected} not found in history")

if __name__ == '__main__':
    main()
