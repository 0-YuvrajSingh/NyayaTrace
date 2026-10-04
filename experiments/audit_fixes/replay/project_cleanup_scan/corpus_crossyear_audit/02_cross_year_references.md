# Cross-year references (read-only grep + code reads)
- scripts/acquire_ecourts_pdfs.py:61-69: year folders mirror SOURCE ARCHIVE layout
  (S3 `data/tar/year={year}/english/`); download per-year tarballs. HISTORICAL (build-time).
- scripts/audit_ecourts_extraction.py:87,104,129-160: globs `year=*` for COUNTS
  (`available_years`, local_pdf_count); dedups by stem (line 133) so one side wins.
  AUDIT_EVIDENCE (counts depend on both sides).
- scripts/clean_and_chunk_ecourts.py:38-39,84-85: reads pdf_dir per year, writes
  cleaned per year; ParquetFile used so `year=` dir is NOT treated as data column.
  HISTORICAL build-time.
- scripts/load_provenance.py:72: reads cleaned per year. HISTORICAL build-time.
- scripts/download_dual_corpus.py:23,102: per-year metadata parquet (source mirror).
- scripts/build_corpus_reports.py:59: per-year metadata parquet reports.
- Runtime (retrieval/infer/eval): NO year-folder references — DB decision_date +
  cleaned chunks + parquet only. ACTIVE_RUNTIME impact of deleting a side: none
  observed, BUT build/audit/count provenance depends on both sides.
- Filenames/hashes/manifests: pair SHAs do not occur elsewhere in repo (02 inventory
  cross-check); 0/5182 overlap nested manifest.
- Classification of references: NO active runtime consumer of raw year-folder PDFs;
  DATASET_MANIFEST + AUDIT_EVIDENCE + HISTORICAL build references exist.
