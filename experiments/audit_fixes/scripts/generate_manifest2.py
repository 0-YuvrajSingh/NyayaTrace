import json, os, hashlib
os.chdir('/repo/experiments/audit_fixes')
m = {}
for f in os.listdir('.'):
    if os.path.isfile(f) and f != 'audit_fixes_manifest.json':
        m[f] = hashlib.sha256(open(f, 'rb').read()).hexdigest()
for root, dirs, files in os.walk('scripts'):
    for f in files:
        p = os.path.join(root, f).replace('\\', '/')
        m[p] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
m['spec_clean/Indian_Legal_XAI_clean.docx'] = hashlib.sha256(open('spec_clean/Indian_Legal_XAI_clean.docx', 'rb').read()).hexdigest()
m['../../Indian_Legal_XAI.docx'] = hashlib.sha256(open('../../Indian_Legal_XAI.docx', 'rb').read()).hexdigest()
with open('/out/audit_fixes_manifest.json', 'w') as f:
    json.dump(m, f, indent=2)
print(json.dumps(m, indent=2))
