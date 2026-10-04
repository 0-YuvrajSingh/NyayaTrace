"""Four-file anomaly probe part 1: file identity + metadata parquet trace (read-only)."""
import hashlib
import json

import pyarrow.parquet as pq
from pypdf import PdfReader

files = [
    "corpus/ecourts/pdfs/year=1979/1980_2_292_297_EN.pdf",
    "corpus/ecourts/pdfs/year=1979/1980_2_293_297_EN.pdf",
    "corpus/ecourts/pdfs/year=1980/1980_2_292_297_EN.pdf",
    "corpus/ecourts/pdfs/year=1980/1980_2_293_297_EN.pdf",
]
inv = []
for f in files:
    raw = open("/repo/" + f, "rb").read()
    try:
        npages = len(PdfReader("/repo/" + f).pages)
    except Exception as e:
        npages = f"ERR {e}"
    inv.append({"path": f, "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "pages": npages})
print(json.dumps(inv, indent=1))

# metadata parquet trace: find rows whose path/stem matches either id
import pyarrow.parquet as pqf

for year in (1979, 1980):
    t = pqf.ParquetFile(f"/repo/corpus/ecourts/metadata/year={year}/metadata.parquet").read()
    print(f"--- metadata year={year}: rows={t.num_rows} cols={t.column_names}")
    rows = t.to_pylist()
    for r in rows:
        blob = json.dumps(r)
        if "292_297" in blob or "293_297" in blob:
            print(json.dumps(r, indent=1)[:1200])
