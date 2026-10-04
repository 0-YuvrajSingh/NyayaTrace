import json

f_paths = []
def recurse(obj):
    if isinstance(obj, dict):
        if 'path' in obj and 'sha256' in obj: f_paths.append(obj['path'])
        for v in obj.values(): recurse(v)
    elif isinstance(obj, list):
        for item in obj: recurse(item)
recurse(json.load(open('/repo/config/reproducibility_freeze.json')))
print("Config paths:", len(f_paths))

a_paths = []
for line in open('/repo/docs/freeze_drift_audit.md').readlines():
    if line.startswith('|'):
        parts = line.split('|')
        if len(parts) > 2 and '`' in parts[2]:
            a_paths.append(parts[2].strip().replace('`', ''))
print("Audit paths:", len(a_paths))

extra = set(f_paths) - set(a_paths)
print("Extra in config (not in audit):")
for p in sorted(extra):
    print("  " + p)
