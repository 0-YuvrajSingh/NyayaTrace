# 05 — Owner-Facing Recommendation: NO_ACTION_CORPUS_QUALITY_NOTE

## Recommendation
### **`NO_ACTION_CORPUS_QUALITY_NOTE`**

Do NOT delete, rename, or modify any of the four PDF files or their associated database/index records.

---

## Rationale and Analysis

1. **Zero Impact on Frozen Evidence (E2, E3, E4):**
   - **E2 Outcome Prediction:** Neither ID (`1980_2_292_297` nor `1980_2_293_297`) appears anywhere in ILDC splits, training checkpoints, or prediction logs.
   - **E3/E4 Retrieval & Grounding:** Neither ID is present in the official 30-case evaluation answer key (`answer_key/authority_answer_key.json`).
   - **Empirical Execution Logs:** Verified `retrieval_results` table in PostgreSQL has exactly 0 records associated with either ID. Neither ID was ever retrieved, ranked, or displayed in the frozen benchmark evaluation.

2. **Reconstruction & Provenance Traceability:**
   - The 39,069-PDF raw corpus count and the per-year acquisition counts in `acquisition_record.json` (426 PDFs for 1979, 406 PDFs for 1980) rely directly on the physical presence of these files in their respective year partitions.
   - Removing any of the four files would break build/audit reproducibility and invalidate documented checksums.

3. **Legal Citation Integrity:**
   - Because the two source IDs represent distinct upstream citations (`[1980] 2 S.C.R. 292` with `1979 INSC 253` vs `[1980] 2 S.C.R. 293` with `1979 INSC 254`), removing one would break citation lookups for valid Supreme Court reporter citations.

4. **Action Items:**
   - Preserve all four files in place.
   - Preserve both source IDs in PostgreSQL and BM25 SQLite.
   - Retain this investigation record as a permanent corpus-quality note.
