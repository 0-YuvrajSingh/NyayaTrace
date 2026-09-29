# 04 — Provenance Determination: DISTINCT_DOCUMENTS_SAME_BYTES

## 1. Upstream-vs-Local Origin Analysis

Investigation of the metadata parquet files (`corpus/ecourts/metadata/year=YYYY/metadata.parquet`), raw e-SCR HTML payloads, and acquisition records establishes that the `1980_2_292_297` versus `1980_2_293_297` distinction originates **100% upstream**:

1. **Upstream e-SCR Portal Metadata:**
   The official Supreme Court digital portal published two distinct records for Civil Appeal No. 1993/1977 (*K. Kalpana Saraswathi v. P.S.S. Somasundram Chettiar*):
   - Record A: Citation `[1980] 2 S.C.R. 292`, Case ID `1979 INSC 253`, CNR `ESCR010001531980`, Disposal `Dismissed`, Languages `ENG,BEN,HIN,PUN`.
   - Record B: Citation `[1980] 2 S.C.R. 293`, Case ID `1979 INSC 254`, CNR `ESCR010002941980`, Disposal `Disposed off`, Languages `ENG,HIN,PUN`.

2. **Upstream S3 Archive Artifacts:**
   The public dataset maintainer (`s3://indian-supreme-court-judgments/`) packaged two distinctly named PDFs (`1980_2_292_297_EN.pdf` and `1980_2_293_297_EN.pdf`) containing the exact same 199,627 bytes. Because of the standard upstream SCR-volume-year vs decision-year dual listing that affects thousands of files from this period, the publisher included both files in both the `year=1979` and `year=1980` tarballs.

3. **Local Ingestion Fidelity:**
   The local acquisition tooling (`scripts/acquire_ecourts_corpus.py`) performed bit-for-bit extraction of the upstream archive. No local step altered filenames, created alias IDs, or synthesized metadata.

---

## 2. Classification

The anomaly is classified as:

### **`DISTINCT_DOCUMENTS_SAME_BYTES`**

### Evidence-Based Elimination:
- **`LOCAL_INGESTION_DUPLICATION` (Eliminated):** Local ingestion did not duplicate any file or introduce extra IDs. The two filenames exist in the upstream archive manifest and per-year source counts.
- **`LOCAL_SOURCE_ID_MISLABELING` (Eliminated):** Both source IDs directly reflect the upstream file paths and official citations. Local processing did not mislabel either ID.
- **`SOURCE_ARCHIVE_DUAL_LISTING` (Eliminated as sole cause):** While dual listing explains why each file appears in both 1979 and 1980 partitions, it does not explain why 292 and 293 coexist as two separate IDs.
- **`UNRESOLVED_PROVENANCE` (Eliminated):** The provenance chain from the official e-SCR court portal HTML through S3 partitions, local acquisition, parquet metadata, cleaned JSONL, PostgreSQL, and SQLite BM25 is fully traced and verified.

### Conclusion:
In official Indian Supreme Court reporting (SCR), consecutive pages in the same volume often report connected orders or substantive judgments arising from the same litigation. In this case, both formal court entries (`1979 INSC 253` and `1979 INSC 254`) share a single scanned 5-page PDF spanning pages 292 to 297. They represent **distinct upstream catalog documents sharing identical bytes**.
