import json, glob

def main():
    paths = glob.glob('/repo/artifacts/week*.json') + glob.glob('/repo/artifacts/dev*.json')
    for path in paths:
        try:
            with open(path) as f:
                data = json.load(f)
            if isinstance(data, dict):
                if 'metadata' in data and 'timestamp' in data['metadata']:
                    print(path, data['metadata']['timestamp'])
                elif 'timestamp' in data:
                    print(path, data['timestamp'])
                elif 'verified_on' in data:
                    print(path, data['verified_on'])
        except Exception:
            pass

if __name__ == '__main__':
    main()
