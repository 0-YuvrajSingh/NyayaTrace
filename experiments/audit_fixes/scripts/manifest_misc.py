"""Show BM25/cache records (read-only)."""
import json

with open("/repo/artifacts/local_cleanup/corpus_consolidation_manifest.json", "rb") as fh:
    doc = json.loads(fh.read().decode("utf-8-sig"))
for r in doc:
    if r["Category"] in ("Bm25Duplicate", "Cache"):
        print(json.dumps(r, indent=1)[:600])
