"""Join git tracked/ignored status into inventory CSV (read-only repo)."""
import csv
from pathlib import Path

OUT = Path("/out/project_cleanup_scan")
rows = list(csv.DictReader(open(OUT / "01_full_inventory.csv", encoding="utf-8")))
def read_list(name):
    for enc in ("utf-8-sig", "utf-16", "utf-8"):
        try:
            return set(x.strip() for x in open(OUT / name, encoding=enc) if x.strip())
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(name)

tracked = read_list("_tracked.txt")
ignored = read_list("_ignored.txt")
for r in rows:
    r["tracked"] = "yes" if r["path"] in tracked else "no"
    r["ignored"] = "yes" if r["path"] in ignored else "no"
with open(OUT / "01_full_inventory.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["path", "size", "ext", "mtime", "sha256", "tracked", "ignored", "executable"])
    w.writeheader()
    w.writerows(rows)
import json
dups = json.load(open(OUT / "_dup_groups.json", encoding="utf-8"))
for g in dups:
    bypath = {r["path"]: r for r in rows if r["path"] in g["paths"]}
    g["tracked"] = [p for p in g["paths"] if bypath.get(p, {}).get("tracked") == "yes"]
print(f"rows={len(rows)} tracked_files_in_inventory={sum(1 for r in rows if r['tracked']=='yes')}")
print(f"dup groups={len(dups)}")
# ext breakdown
from collections import Counter
c = Counter(r["ext"] for r in rows)
print("top ext:", c.most_common(12))
# dir breakdown
d = Counter(r["path"].split("/")[0] for r in rows)
print("top dirs:", d.most_common(15))
