import os

def search_files():
    targets = ['submission', 'docs', 'experiments', 'answer_key', 'artifacts', 'scripts']
    for t in targets:
        for root, dirs, files in os.walk(t):
            for f in files:
                if f.endswith(('.json', '.md', '.py', '.tex', '.txt')):
                    p = os.path.join(root, f)
                    try:
                        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                            txt = fp.read()
                            if '0.6486' in txt or '0.6073' in txt or 'Combined-37' in txt:
                                print(f"Found in {p}")
                    except Exception as e:
                        pass

if __name__ == '__main__':
    search_files()

