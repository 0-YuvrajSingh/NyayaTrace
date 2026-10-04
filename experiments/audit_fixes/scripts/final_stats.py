"""Count final PDF pages/words."""
from pypdf import PdfReader

r = PdfReader("/out/paper_master_final.pdf")
texts = [(p.extract_text() or "") for p in r.pages]
full = " ".join(texts)
print("final pages:", len(r.pages))
print("final words:", len(full.split()))
