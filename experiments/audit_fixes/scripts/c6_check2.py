import json, os, hashlib

f_paths = {}
def recurse(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj: f_paths[obj['path']] = obj['sha256']
        for v in obj.values(): recurse(v)
    elif isinstance(obj, list):
        for item in obj: recurse(item)
recurse(json.load(open('/repo/config/reproducibility_freeze.json')))

a_paths = []
for line in open('/repo/docs/freeze_drift_audit.md').readlines():
    if line.startswith('|'):
        parts = line.split('|')
        if len(parts) > 2 and '`' in parts[2]:
            path = parts[2].strip().replace('`', '')
            if '/' in path or '.' in path:
                a_paths.append(path)

extra = set(f_paths.keys()) - set(a_paths)
print("The 4 extra paths in config:")
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
