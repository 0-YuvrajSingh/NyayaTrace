import json, hashlib, os

def get_sha256(path):
    if not os.path.exists(path): return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_sha256_lf(path):
    if not os.path.exists(path): return None
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        content = f.read().replace(b'\r\n', b'\n')
        h.update(content)
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
    
    print("| Path | Expected | Actual | Actual after CRLF->LF | Status |")
    print("|---|---|---|---|---|")
    
    for path, expected in paths_to_sha.items():
        full_path = '/repo/' + path
        actual = get_sha256(full_path)
        actual_lf = get_sha256_lf(full_path)
        
        status = 'MISSING'
        if actual is not None:
            if actual == expected:
                status = 'EXACT'
            elif actual_lf == expected:
                status = 'EOL_ONLY'
            else:
                status = 'DRIFT'
        
        print(f"| `{path}` | `{expected}` | `{actual if actual else 'MISSING'}` | `{actual_lf if actual_lf else 'MISSING'}` | {status} |")

if __name__ == '__main__':
    main()
