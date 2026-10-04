# 02 — parse check (BOM is the only defect; NOT repaired)
- UTF-8 BOM present (EF BB BF). Strict utf-8 parse FAILS at char 0
  ("Unexpected UTF-8 BOM ... line 1 column 1").
- utf-8-sig parse: OK. Hypothetical BOM removal yields valid JSON (verified in
  memory only; original bytes untouched).
- Content: JSON list, 3,529 records, uniform schema:
  Category, SourcePath, DestinationPath, SourceSize, SourceSha256,
  DestinationExisted, DestinationSha256, Action.
- Actions: REMOVE_PROVEN_DUPLICATE_PDF 3460; REMOVE_PROVEN_DUPLICATE_CHUNKS 44;
  REMOVE_PROVEN_DOWNLOAD_DUPLICATE 21; REMOVE_PROVEN_DUPLICATE_BM25 1;
  REMOVE_PYTHON_CACHE 3.
