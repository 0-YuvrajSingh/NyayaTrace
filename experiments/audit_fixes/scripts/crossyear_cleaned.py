"""Check which pair sides were cleaned/indexed (read-only)."""
import json

with open("/repo/experiments/audit_fixes/replay/project_cleanup_scan/_dup_groups.json") as fh:
    dups = json.load(fh)
pairs = []
for g in dups:
    ps = [p for p in g["paths"] if p.startswith("corpus/ecourts/pdfs/year=")]
    if len(ps) == 2 and len(g["paths"]) == 2:
        pairs.append((ps[0], ps[1]))
print("sample 6 pairs, checking cleaned presence + chunk linkage:")
import os
for a, b in pairs[:6]:
    for p in (a, b):
        print(" ", p, "exists" if os.path.exists("/repo/" + p) else "MISSING")
print("done (DB chunk check via SQL next)")
