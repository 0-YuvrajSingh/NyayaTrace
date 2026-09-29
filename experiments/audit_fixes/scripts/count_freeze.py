import json

def main():
    for p in ['/repo/config/reproducibility_freeze.json', '/repo/validation_replay/freeze_validation.json']:
        with open(p) as f:
            data = json.load(f)
        if 'items' in data:
            print(f'{p}: {len(data["items"])} entries')
            counts = {}
            for x in data['items']:
                st = x.get('status', 'unknown')
                counts[st] = counts.get(st, 0) + 1
            print(counts)
        else:
            paths = []
            def recurse(obj):
                if isinstance(obj, dict):
                    if 'path' in obj and 'sha256' in obj:
                        paths.append(obj)
                    for v in obj.values(): recurse(v)
                elif isinstance(obj, list):
                    for item in obj: recurse(item)
            recurse(data)
            print(f'{p}: {len(paths)} entries (paths with sha256)')

if __name__ == '__main__':
    main()
