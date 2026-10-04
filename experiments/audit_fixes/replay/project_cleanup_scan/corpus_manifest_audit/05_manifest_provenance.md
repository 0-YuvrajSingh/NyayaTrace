# 05 — provenance (read-only evidence)
- Generated ~2026-09-19 (mtime) during a local cleanup pass; documents an EXECUTED
  operation, not a plan: 0/3529 SourcePaths still exist; 3526/3529 DestinationPaths exist.
- What it documents: removal of proven nested duplicates — paths like
  corpus\corpus\corpus\corpus\ecourts\pdfs\…(1).pdf (3,460), nested chunk copies (44),
  canonical download dupes (21), a duplicate BM25 file retrieval\bm25-001.sqlite (1),
  pycache dirs (3).
- Why it matters: the ONLY surviving per-file record (with SHAs) of what was removed.
  Directly scopes the pending 5,182 cross-year dup analysis: those pairs are a
  DIFFERENT phenomenon (distinct year folders, both sides present) from the nested
  copies already resolved here. Deleting this file would erase that distinction.
- Reproducibility from survivors: partial (destinations + SHAs persist) but the
  removed-source list itself is unique and non-reconstructible.
