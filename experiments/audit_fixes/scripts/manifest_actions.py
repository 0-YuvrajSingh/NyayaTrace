"""Manifest action distribution + existence check (read-only)."""
import json
import os
from collections import Counter

doc = json.loads(open("/repo/artifacts/local_cleanup/corpus_consolidation_manifest.json", "rb").read().decode("utf-8-sig"))
print("actions:", dict(Counter(r["Action"] for r in doc)))
print("categories:", dict(Counter(r["Category"] for r in doc)))
# normalize windows separators to check existence (read-only stat)
import pathlib
def norm(p):
    return "/repo/" + str(p).replace("\\", "/") if p else None
still_src = sum(1 for r in doc if norm(r["SourcePath"]) and os.path.exists(norm(r["SourcePath"])))
still_dst = sum(1 for r in doc if norm(r["DestinationPath"]) and os.path.exists(norm(r["DestinationPath"])))
print(f"records={len(doc)} source-still-exists={still_src} dest-still-exists={still_dst}")
print("sample destinations:", [r["DestinationPath"] for r in doc[:3]])
