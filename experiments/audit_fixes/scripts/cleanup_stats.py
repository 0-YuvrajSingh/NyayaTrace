"""Scan stats: 6page pdf, badjson, empty, dir sizes."""
import csv
import json
from collections import Counter
from pypdf import PdfReader

try:
    r = PdfReader("/repo/paper_master_6page.pdf")
    t = " ".join([(p.extract_text() or "") for p in r.pages])
    print("6page:", len(r.pages), "pages,", len(t.split()), "words")
except Exception as e:
    print("6page ERR", e)

print("badjson:", json.load(open("/out/project_cleanup_scan/_badjson.json")))
print("empty:", json.load(open("/out/project_cleanup_scan/_empty.json"))[:25])

rows = list(csv.DictReader(open("/out/project_cleanup_scan/01_full_inventory.csv")))
d = {}
for r in rows:
    top = r["path"].split("/")[0]
    dd = d.setdefault(top, [0, 0])
    dd[0] += 1
    dd[1] += int(r["size"]) if int(r["size"]) > 0 else 0
for k in sorted(d):
    print(k, d[k][0], d[k][1])
