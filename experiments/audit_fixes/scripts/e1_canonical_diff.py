"""E1 canonical diff: prove runs differ only in model_artifact path field."""
from __future__ import annotations
import json, hashlib

def load_strip(path: str) -> dict:
    d = json.load(open(path))
    d.pop("model_artifact", None)
    # strip from each record too, if present
    for rec in d.get("records", []):
        rec.pop("model_artifact", None)
    return d

r1 = load_strip("/out/e1_test1.json")
r2 = load_strip("/out/e1_test2.json")

h1 = hashlib.sha256(json.dumps(r1, sort_keys=True).encode()).hexdigest()
h2 = hashlib.sha256(json.dumps(r2, sort_keys=True).encode()).hexdigest()
print(f"canonical hash run1: {h1}")
print(f"canonical hash run2: {h2}")
print("canonical JSON: " + ("IDENTICAL" if h1 == h2 else "DIFFERS"))

m1 = r1.get("reproduced_metrics", {})
m2 = r2.get("reproduced_metrics", {})
print("metrics: " + ("IDENTICAL" if m1 == m2 else f"DIFFERS: {m1} vs {m2}"))

preds1 = [rec.get("prediction") for rec in r1.get("records", [])]
preds2 = [rec.get("prediction") for rec in r2.get("records", [])]
print("prediction arrays length: run1=%d run2=%d" % (len(preds1), len(preds2)))
print("prediction arrays: " + ("IDENTICAL" if preds1 == preds2 else "DIFFERS"))
print("all other keys: " + ("IDENTICAL" if r1 == r2 else "DIFFERS"))
