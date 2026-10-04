"""Manifest integrity + content probe (read-only; no writes to source)."""
import hashlib
import json

p = "/repo/artifacts/local_cleanup/corpus_consolidation_manifest.json"
raw = open(p, "rb").read()
print("bytes:", len(raw))
print("sha256:", hashlib.sha256(raw).hexdigest())
print("BOM present:", raw[:3] == b"\xef\xbb\xbf")
try:
    json.loads(raw.decode("utf-8"))
    print("strict utf-8 parse: OK")
except Exception as e:
    print("strict utf-8 parse FAIL:", str(e)[:150])
try:
    doc = json.loads(raw.decode("utf-8-sig"))
    print("utf-8-sig parse: OK")
    print("top-level type:", type(doc).__name__)
    if isinstance(doc, dict):
        print("top-level keys:", list(doc.keys()))
        for k, v in doc.items():
            if isinstance(v, list):
                print(f"key {k!r}: list len={len(v)} first-item-keys={list(v[0].keys()) if v and isinstance(v[0], dict) else type(v[0]).__name__ if v else 'empty'}")
            elif isinstance(v, dict):
                print(f"key {k!r}: dict subkeys={list(v.keys())[:12]}")
            else:
                print(f"key {k!r}: {type(v).__name__}={repr(v)[:120]}")
    elif isinstance(doc, list):
        print("list len:", len(doc))
except Exception as e:
    print("utf-8-sig parse FAIL:", str(e)[:150])
