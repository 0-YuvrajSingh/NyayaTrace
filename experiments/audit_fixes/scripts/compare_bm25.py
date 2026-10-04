import json

def compare_canonical(f1, f2, ignore_keys):
    try:
        d1 = json.load(open(f1))
        d2 = json.load(open(f2))
        for k in ignore_keys:
            d1.pop(k, None)
            d2.pop(k, None)
        s1 = json.dumps(d1, sort_keys=True)
        s2 = json.dumps(d2, sort_keys=True)
        if s1 == s2:
            print(f"{f1} and {f2} are IDENTICAL (canonical)")
        else:
            print(f"{f1} and {f2} DIFFER")
            # print("  File 1:", s1)
            # print("  File 2:", s2)
    except Exception as e:
        print(f"Error comparing {f1} and {f2}: {e}")

compare_canonical('/repo/artifacts/bm25_index.json', '/out/bm25_index.json', ['built_at_utc'])
compare_canonical('/repo/artifacts/ecourts_corpus_identity.json', '/out/ecourts_corpus_identity.json', ['timestamp', 'identity_version', 'evaluation_version', 'versions'])
