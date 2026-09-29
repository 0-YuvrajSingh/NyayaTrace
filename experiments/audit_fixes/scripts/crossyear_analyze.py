"""Cross-year pair analysis (read-only)."""
import csv
import json
import re
from collections import Counter
from pathlib import Path

R = Path("/repo")
dups = json.load(open("/repo/experiments/audit_fixes/replay/project_cleanup_scan/_dup_groups.json"))
pairs = []
for g in dups:
    ps = [p for p in g["paths"] if p.startswith("corpus/ecourts/pdfs/year=")]
    if len(ps) == 2 and len(g["paths"]) == 2:
        pairs.append((ps[0], ps[1], g["size"], g["sha256"]))
print("clean 2-path pdf pairs:", len(pairs))
other = [g for g in dups if not (len([p for p in g["paths"] if p.startswith("corpus/ecourts/pdfs/year=")]) == 2 and len(g["paths"]) == 2) and any(p.startswith("corpus/ecourts/pdfs/") for p in g["paths"])]
print("other pdf-involved groups:", len(other))
for g in other[:10]:
    print("  ", g["size"], g["paths"])

def year(p):
    m = re.search(r"year=(\d{4})", p)
    return int(m.group(1)) if m else None

yp = Counter()
pat = Counter()
for a, b, s, h in pairs:
    ya, yb = year(a), year(b)
    yp[(min(ya, yb), max(ya, yb))] += 1
    fa, fb = a.split("/")[-1], b.split("/")[-1]
    pat["same_filename" if fa == fb else "diff_filename"] += 1
print("filename pattern:", dict(pat))
print("distinct year-pairs:", len(yp))
print("top year-pairs:", yp.most_common(12))
# year gap distribution
gap = Counter(abs(a - b) for (a, b) in yp for _ in range(1))
gap2 = Counter()
for (a, b), c in yp.items():
    gap2[abs(a - b)] += c
print("gap distribution:", dict(sorted(gap2.items())))

with open("/out/project_cleanup_scan/corpus_crossyear_audit/01_cross_year_pair_inventory.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["left_path", "right_path", "left_year", "right_year", "year_gap", "same_filename", "size", "sha256"])
    for a, b, s, h in sorted(pairs):
        ya, yb = year(a), year(b)
        w.writerow([a, b, ya, yb, abs(ya - yb), a.split("/")[-1] == b.split("/")[-1], s, h])
print("inventory written")

with open("/out/project_cleanup_scan/corpus_crossyear_audit/03_year_pair_breakdown.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["year_a", "year_b", "gap", "count"])
    for (a, b), c in sorted(yp.items()):
        w.writerow([a, b, abs(a - b), c])
print("breakdown written")

# nested-cleanup distinction: any pair path with (1) or corpus/corpus? any pair SHA in manifest?
man = json.loads(open("/repo/artifacts/local_cleanup/corpus_consolidation_manifest.json", "rb").read().decode("utf-8-sig"))
mshas = set(r["SourceSha256"] for r in man if r["SourceSha256"]) | set(r["DestinationSha256"] for r in man if r["DestinationSha256"])
nested_mark = sum(1 for a, b, s, h in pairs if "(1)" in a or "(1)" in b or "corpus/corpus" in a)
overlap = sum(1 for a, b, s, h in pairs if h in mshas)
print(f"pairs with nested markers: {nested_mark}/5182; pair SHAs in manifest: {overlap}/5182")
