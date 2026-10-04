# 02 — Source Metadata Trace (Read-Only)

Comprehensive provenance and metadata trace for candidate source IDs `1980_2_292_297` and `1980_2_293_297`.

---

## 1. Per-Year Metadata Parquet (`corpus/ecourts/metadata/year=YYYY/metadata.parquet`)

Both candidate IDs are present in both `year=1979` and `year=1980` metadata parquet files with distinct upstream records:

### `1980_2_292_297`
- **Title:** `K. KALPANA SARASWATHI versus P. S. S. SOMASUNDRAM CHETTIAR`
- **Citation:** `[1980] 2 S.C.R. 292`
- **Case ID / Neutral Citation:** `1979 INSC 253` (`nc_display`: `1979INSC253`)
- **CNR:** `ESCR010001531980`
- **Decision Date:** `29-11-1979`
- **Disposal Nature:** `Dismissed`
- **Court:** `Supreme Court of India`
- **Judge:** `V.R. KRISHNA IYER` (Coram in HTML: `V.R. KRISHNA IYER*`, `R.S. PATHAK`)
- **Available Languages:** `ENG,BEN,HIN,PUN` (Bengali included)
- **Case No (from e-SCR HTML):** `CIVIL APPEAL No. 1993/1977`
- **Raw HTML links:** `link_1` / `link_52`; calls `get_pdf_lang(..., '1980_2_292_297', '1980')` and `open_pdf(..., '1980', '1980_2_292_297', '1979INSC253')`

### `1980_2_293_297`
- **Title:** `K. KALPANA SARASWATHI versus P. S. S. SOMASUNDRAM CHETTIAR`
- **Citation:** `[1980] 2 S.C.R. 293`
- **Case ID / Neutral Citation:** `1979 INSC 254` (`nc_display`: `1979INSC254`)
- **CNR:** `ESCR010002941980`
- **Decision Date:** `29-11-1979`
- **Disposal Nature:** `Disposed off` (*differs from Dismissed*)
- **Court:** `Supreme Court of India`
- **Judge:** `V.R. KRISHNA IYER` (Coram in HTML: `V.R. KRISHNA IYER*`, `R.S. PATHAK`)
- **Available Languages:** `ENG,HIN,PUN` (*Bengali not listed*)
- **Case No (from e-SCR HTML):** `CIVIL APPEAL No. 1993/1977`
- **Raw HTML links:** `link_0` / `link_51`; calls `get_pdf_lang(..., '1980_2_293_297', '1980')` and `open_pdf(..., '1980', '1980_2_293_297', '1979INSC254')`

**Key finding:** The distinction between 292 and 293 is an upstream metadata distinction. They possess distinct neutral citations (`1979 INSC 253` vs `254`), distinct SCR page citations (`292` vs `293`), distinct CNR numbers, distinct disposal natures, and distinct language options.

---

## 2. Acquisition Records (`corpus/ecourts/acquisition_record.json`)

- **Year 1979:** `source_file_count: 426`, `source_archive_bytes: 252866560`, `new_pdfs_extracted: 426`, `local_pdf_count: 426`.
- **Year 1980:** `source_file_count: 406`, `source_archive_bytes: 266874880`, `new_pdfs_extracted: 406`, `local_pdf_count: 406`.
- Both `1980_2_292_297_EN.pdf` and `1980_2_293_297_EN.pdf` were individually unpacked from the official upstream AWS S3 archive partitions (`s3://indian-supreme-court-judgments/`) for both years.
- Neither filename was generated or altered by local acquisition scripts.

---

## 3. Cleaning Records & Chunk Records (`corpus/ecourts/cleaning_record.json` & `corpus/ecourts/cleaned/`)

- Cleaning pipeline (`v1-conservative-page-text`) processed both files in both year partitions:
  - `corpus/ecourts/cleaned/year=1979/chunks.jsonl`: 28 chunks for `1980_2_292_297`, 28 chunks for `1980_2_293_297`.
  - `corpus/ecourts/cleaned/year=1980/chunks.jsonl`: 28 chunks for `1980_2_292_297`, 28 chunks for `1980_2_293_297`.
- Across all 4 files, the chunk text, character offsets, and page boundaries are identical:
  - Total chunks: 28 per source ID.
  - Page span: Pages 1 to 5.
  - Total concatenated chunk text length: 13,284 characters.
  - Concatenated chunk text MD5: `8d16e507dc1b126fddf8e970b6c58556`.

---

## 4. Database Provenance Fields (`corpus_chunks` in PostgreSQL)

- Table `corpus_chunks` indexed both source IDs from `cleaned/year=1979/chunks.jsonl`:
  - `1980_2_292_297`: 28 rows, primary key `1980_2_292_297::p0001::c001` .. `c028`.
  - `1980_2_293_297`: 28 rows, primary key `1980_2_293_297::p0001::c001` .. `c028`.
- Total rows in `corpus_chunks`: 56 rows (28 + 28).
- The year=1980 duplicates were rejected at load time by the primary key `chunk_id` constraint, preserving the year=1979 rows.
- Because `source_id` is prefixed in `chunk_id`, the database does **not** collapse the two IDs; both coexist in `corpus_chunks`.

---

## 5. Retrieval Index (`retrieval/bm25.sqlite`)

- `chunk_temporal_metadata`: Holds 28 chunks for `1980_2_292_297` and 28 chunks for `1980_2_293_297` (decision year 1979 for both).
- `chunks_fts`: Indexes both 28-chunk sets under their respective `chunk_id`s.
- The retrieval index retains both IDs; it does not collapse them.

---

## 6. Manifests, Reports, and Frozen Experimental Records

- `corpus/dataset_manifest.md`: Includes the 39,069-PDF corpus count; neither ID is excluded or flagged.
- `corpus/dedup_matches.csv`: Zero occurrences (neither ID maps to an ILDC query).
- `corpus/dedup_report.md`: Zero occurrences.
- `answer_key/authority_answer_key.json`: Zero occurrences (neither ID is a reference authority).
- `retrieval_results` (PostgreSQL table): Zero occurrences (`count = 0`). Neither ID was retrieved or selected in frozen benchmark runs.
- Frozen E2/E3/E4 training/test sets: Zero occurrences.
