import json, os, hashlib

def get_freeze_paths():
    data = json.load(open('/repo/config/reproducibility_freeze.json'))
    paths = {}
    def recurse(obj):
        if isinstance(obj, dict):
            if 'path' in obj and 'sha256' in obj: paths[obj['path']] = obj['sha256']
            for v in obj.values(): recurse(v)
        elif isinstance(obj, list):
            for item in obj: recurse(item)
    recurse(data)
    return paths

def get_audit_paths():
    content = open('/repo/docs/freeze_drift_audit.md').read()
    paths = []
    for line in content.split('\n'):
        if line.startswith('|') and '`' in line:
            parts = line.split('|')
            if len(parts) > 2 and '`' in parts[2]:
                paths.append(parts[2].strip().replace('`', ''))
    return paths

f_paths = get_freeze_paths()
a_paths = get_audit_paths()
a_paths = [p for p in a_paths if p in f_paths]
print('C6: 43 in config vs', len(a_paths), 'in audit table')
extra = set(f_paths.keys()) - set(a_paths)
print('Extra paths:', extra)
for p in extra:
    full_path = '/repo/' + p
    if os.path.exists(full_path):
        actual = hashlib.sha256(open(full_path, 'rb').read()).hexdigest()
        actual_lf = hashlib.sha256(open(full_path, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()
        if actual == f_paths[p]:
            print(f'  {p} exists, EXACT')
        elif actual_lf == f_paths[p]:
            print(f'  {p} exists, EOL_ONLY')
        else:
            print(f'  {p} exists, DRIFT')
    else:
        print(f'  {p} missing')

print('\nC7: Check corpus/dataset_manifest.md')
p = 'corpus/dataset_manifest.md'
full_path = '/repo/' + p
if os.path.exists(full_path):
    actual = hashlib.sha256(open(full_path, 'rb').read()).hexdigest()
    actual_lf = hashlib.sha256(open(full_path, 'rb').read().replace(b'\r\n', b'\n')).hexdigest()
    if actual == f_paths.get(p): print(f'{p}: EXACT')
    elif actual_lf == f_paths.get(p): print(f'{p}: EOL_ONLY')
    else: print(f'{p}: DRIFT')

print('\nC10: Top-level keys, sizes, counts of DRIFT files')
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
for p in drift_files:
    full_path = '/repo/' + p
    if not os.path.exists(full_path): continue
    size = os.path.getsize(full_path)
    print(f'-- {p} ({size} bytes) --')
    if p.endswith('.json'):
        data = json.load(open(full_path))
        print('Keys:', list(data.keys()))
        if isinstance(data, dict):
            for k in ['built_at_utc', 'versions', 'evaluation_version', 'timestamp']:
                if k in data: print(f'{k}: {data[k]}')
    elif p.endswith('.md'):
        lines = open(full_path).readlines()
        print('Lines:', len(lines))
