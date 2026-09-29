"""Count revised PDF pages/words (read-only /repo, /out)."""
from pypdf import PdfReader

r = PdfReader("/out/paper_master_revised.pdf")
texts = [(p.extract_text() or "") for p in r.pages]
full = " ".join(texts)
print("revised pages:", len(r.pages))
print("revised words:", len(full.split()))
