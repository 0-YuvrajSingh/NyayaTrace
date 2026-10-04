"""Per-page word counts for final PDF."""
from pypdf import PdfReader

r = PdfReader("/out/paper_master_final.pdf")
for i, p in enumerate(r.pages):
    t = p.extract_text() or ""
    print(f"page {i+1}: {len(t.split())} words | {t[:90]!r}")
