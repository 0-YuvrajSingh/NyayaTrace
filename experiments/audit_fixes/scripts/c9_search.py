import json, os, hashlib

data = json.load(open('/repo/config/reproducibility_freeze.json'))
expected_hashes = set()
def recurse(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj: expected_hashes.add(obj['sha256'])
        for v in obj.values(): recurse(v)
    elif isinstance(obj, list):
        for item in obj: recurse(item)
recurse(data)

found_matches = []
for root, dirs, files in os.walk('/repo'):
    if '.git' in root or 'node_modules' in root: continue
    for f in files:
        if 'submission' in root or f.endswith('.zip') or f.endswith('.bak') or f.endswith('.tar.gz'):
            full_path = os.path.join(root, f)
            try:
                content = open(full_path, 'rb').read()
                h = hashlib.sha256(content).hexdigest()
                hlf = hashlib.sha256(content.replace(b'\r\n', b'\n')).hexdigest()
                if h in expected_hashes or hlf in expected_hashes:
                    found_matches.append((full_path, h))
            except: pass
print('C9 Matches found:')
for m in found_matches:
    print(' ', m)
