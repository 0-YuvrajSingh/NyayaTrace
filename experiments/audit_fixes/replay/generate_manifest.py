import hashlib, os, json

def main():
    os.chdir('/out/experiments/audit_fixes')
    manifest = {}
    for root, _, files in os.walk('.'):
        for f in files:
            if f == 'audit_fixes_manifest.json': continue
            path = os.path.normpath(os.path.join(root, f)).replace('\\', '/')
            with open(path, 'rb') as fp:
                manifest[path] = hashlib.sha256(fp.read()).hexdigest()
    
    with open('/out/Indian_Legal_XAI.docx', 'rb') as fp:
        manifest['../../Indian_Legal_XAI.docx'] = hashlib.sha256(fp.read()).hexdigest()

    with open('audit_fixes_manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)

if __name__ == '__main__':
    main()
