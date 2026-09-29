"""Manifest content schema probe (read-only)."""
import json
from collections import Counter

doc = json.loads(open("/repo/artifacts/local_cleanup/corpus_consolidation_manifest.json", "rb").read().decode("utf-8-sig"))
print("records:", len(doc))
print("first record keys:", list(doc[0].keys()))
import pprint
pprint.pprint(doc[0])
print("---last record keys:", list(doc[-1].keys()))
ks = Counter()
for r in doc:
    if isinstance(r, dict):
        for k in r:
            ks[k] += 1
print("key frequency:", dict(ks))
