# Reproduction impact (computed, no data modified)
- 5,182 groups (5,181 pairs + 1 four-file group); 81 distinct year-pairs; gap 1 = 5,134.
- Unique physical PDFs: pair SHAs are distinct per group observed (no cross-group SHA
  check run exhaustively — assume per-group unique pending owner phase).
- Runtime metrics (E2/E3/retrieval): NO impact from either-side deletion (single
  logical source_id per pair already; DB/cleaned/parquet unaffected).
- Corpus construction/audit reproducibility: IMPACT — per-year acquisition counts,
  audit availability counts, and any re-run of acquire/audit/clean provenance would
  diverge (counts, folder walks). 39,069-PDF count traceability requires both sides.
- Training/validation/test composition: no impact (ILDC parquet separate).
- Temporal evaluation: no impact (decision_date from metadata/DB, never folder year;
  dataset manifest explicitly warns against inferring year from identifiers/paths).
- Frozen manifests: pair PDFs are raw-source level, below frozen chunk identity
  (2,036,981 unique chunks); no pair SHA found in frozen chunk/manifest records checked.
- E2/E3 audited corpus: unaffected (single-source resolution already in DB).
