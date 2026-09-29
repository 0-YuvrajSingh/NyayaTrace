import json, hashlib, os, glob

def get_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    with open('/repo/config/reproducibility_freeze.json') as f:
        data = json.load(f)
        
    paths_to_sha = {}
    def recurse(obj):
        if isinstance(obj, dict):
            if 'path' in obj and 'sha256' in obj:
                paths_to_sha[obj['path']] = obj['sha256']
            for v in obj.values():
                recurse(v)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)
    recurse(data)
    
    # Collect files to check
    files_to_check = []
    files_to_check.extend(glob.glob('/repo/artifacts/**/*', recursive=True))
    files_to_check.extend(glob.glob('/repo/checkpoints/**/*', recursive=True))
    files_to_check.extend(glob.glob('/repo/*.sqlite'))
    
    files_to_check = [f for f in files_to_check if os.path.isfile(f)]
    
    mismatches = []
    checked = 0
    not_in_freeze = []
    for f in files_to_check:
        rel_path = os.path.relpath(f, '/repo').replace('\\', '/')
        if rel_path in paths_to_sha:
            expected = paths_to_sha[rel_path]
            actual = get_sha256(f)
            checked += 1
            if expected != actual:
                mismatches.append(f"{rel_path}: expected {expected}, got {actual}")
        else:
            not_in_freeze.append(rel_path)
            
    print(f"Checked {checked} files that are present in both the filesystem and the freeze manifest.")
    if mismatches:
        print("MISMATCHES FOUND:")
        for m in mismatches:
            print("  " + m)
    else:
        print("No mismatches found among files present in both.")
    
    # Check for missing files
    missing = [p for p in paths_to_sha if p.startswith(('artifacts/', 'checkpoints/')) or p.endswith('.sqlite')]
    missing = [p for p in missing if not os.path.exists('/repo/' + p)]
    if missing:
        print("FILES IN FREEZE BUT MISSING ON DISK:")
        for m in missing:
            print("  " + m)

if __name__ == '__main__':
    main()
