"""Count 6-page PDF pages/words + per-page density."""
from pypdf import PdfReader

r = PdfReader("/out/paper_master_6page.pdf")
texts = [(p.extract_text() or "") for p in r.pages]
full = " ".join(texts)
print("pages:", len(r.pages))
print("words:", len(full.split()))
for i, p in enumerate(r.pages):
    t = p.extract_text() or ""
    print(f"page {i+1}: {len(t.split())} words | {t[:80]!r}")
