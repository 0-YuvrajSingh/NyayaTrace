"""Paper inventory stats (read-only /repo)."""
from pypdf import PdfReader

r = PdfReader("/repo/paper_master.pdf")
print("pages:", len(r.pages))
texts = [(p.extract_text() or "") for p in r.pages]
full = "\n".join(texts)
print("pdf_words:", len(full.split()))
print("pdf_chars:", len(full))
