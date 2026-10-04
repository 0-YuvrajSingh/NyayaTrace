# 03 — Final Repository-Wide Cleanup Report

Comprehensive accounting of the final repository-wide cleanup execution and residual audit for NyayaTrace.

---

## 1. Executive Summary & Quantitative Delta

| Metric | Pre-Cleanup Baseline | Post-Cleanup State | Net Delta |
|:---|---:|---:|---:|
| **Non-Git File Count** | 40,004 | 39,999 | **-5 net** (-8 deleted, +3 audit files) |
| **Non-Git Directory Count** | 327 | 327 | **0 net** (`artifacts/figures` removed, `final_cleanup` added) |
| **Total Non-Git Volume** | 31,287,505,034 bytes | 31,287,242,786 bytes | **-262,248 bytes** (-281,649 bytes deleted) |
| **Git Tracked Files** | 459 | 454 | **-5 tracked files** (5 duplicate figures removed) |
| **Corpus PDF Count** | 39,068 | 39,068 | **0 (Zero mutation)** |
| **Corpus Parquet Count** | 74 | 74 | **0 (Zero mutation)** |
| **Active Secrets Remaining** | 1 (`.db_env`) | 0 | **-1 (Completely eliminated)** |

---

## 2. Executed Approved Deletions (8 Files, 281,649 Bytes Removed)

The owner explicitly authorized the removal of 4 target items (covering 8 physical files):

1. **`experiments/audit_fixes/replay/.db_env` (132 bytes; SHA-256: `d2cb3b420...`):**
   - **Rationale:** Live database credential created during Phase 16 audit replay. No active runtime consumers; credentials intentionally excluded from scientific reproducibility freeze.
   - **Action Taken:** Permanently deleted.

2. **`paper_master_6page.tex` (31,746 bytes; SHA-256: `53084d973...`):**
   - **Rationale:** Obsolete alternate manuscript that reintroduced unsupported claims and overfull boxes; superseded by `paper_master_final.tex`.
   - **Action Taken:** Permanently deleted.

3. **`paper_master_6page.pdf` (222,823 bytes; SHA-256: `a05316a2b...`):**
   - **Rationale:** Obsolete compiled PDF corresponding to the deleted 6page source.
   - **Action Taken:** Permanently deleted.

4. **`artifacts/figures/*` (5 files, 26,948 bytes total):**
   - `artifacts/figures/week14_figure_a_outcome_prediction.svg` (5,938 bytes; SHA-256: `489d0fd2...`)
   - `artifacts/figures/week14_figure_b_retrieval_funnel.svg` (2,723 bytes; SHA-256: `828b0bc5...`)
   - `artifacts/figures/week14_figure_c_retrieval_investigation.svg` (8,354 bytes; SHA-256: `6fb159c2...`)
   - `artifacts/figures/week14_figure_d_integrity_summary.svg` (4,017 bytes; SHA-256: `c4c5bba1...`)
   - `artifacts/figures/week14_figure_e_explanation_review.svg` (5,916 bytes; SHA-256: `1f1cc72d...`)
   - **Rationale:** Exact duplicates of authoritative vector figures preserved in `submission/figures/`. No manuscript referenced `artifacts/figures/`.
   - **Action Taken:** All 5 files permanently deleted; empty directory removed.

---

## 3. Preserved Canonical Research Artifacts

- **Canonical Publication Manuscript:**
  - `paper_master_final.tex` (37,222 bytes; SHA-256: `FADC2392166664C60FB18365557BF065123AD62DE476F81A94DA3FAC236F961C`)
  - `paper_master_final.pdf` (204,518 bytes; SHA-256: `93EECD93CBD2EA8D98266703E93D020B656C986858C282DC3326193F75EDB712`)
- **Audit Baseline Manuscript:**
  - `paper_master.tex` (55,994 bytes; SHA-256: `9DE053A7C74F8807D86100C5D2FB9C93DDB602EFC140EE59B9808903D0F06D2A`)
  - `paper_master.pdf` (293,984 bytes; SHA-256: `3B35C27966D72EE7DABECBA6329A771E71ADBBBCA03E3DCAF1D721E97763EBBD`)
- **Canonical Figures:**
  - `figures/fig1_outcome.pdf` through `fig5_explanation.pdf` (5 PDF figures)
  - `submission/figures/week14_figure_a_*.svg` through `figure_e_*.svg` (5 SVG vector sources)
- **Scientific Models & Retrieval Index:**
  - `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/model.safetensors` (437,958,648 bytes; SHA-256: `924A5BB9078BCC212EF07ACB9F08DFAA8593E880AE3868203DEB28586DBDC773`)
  - `retrieval/bm25.sqlite` (2,269,376,512 bytes; SHA-256: `3187F7FCE824EA8CCC5A26D908936CE4B78E81238289EA69348CB861350D65FB`)
- **Evaluation Standards:**
  - `answer_key/authority_answer_key.json` (30 verified ground-truth cases)
  - `artifacts/e2_chunk_pool_results.json` & `artifacts/e3_e4_evidence_augmented_evaluation.json`

---

## 4. Blocked Items (Preserved Under Policy Rules)

### A. Blocked Pending Archive Destination (5 Files)
Per prompt instructions, obsolete items approved *only* for archival cannot be deleted without an established archive structure:
1. `paper_master_revised.tex` (56,898 bytes) — superseded manuscript draft.
2. `paper_master_revised.pdf` (294,801 bytes) — compiled PDF of superseded draft.
3. `Indian_Legal_XAI.docx` (27,166 bytes) — obsolete initial proposal/spec.
4. `experiments/audit_fixes/replay/paper_master_original_backup.tex` (55,994 bytes) — duplicate backup of baseline.
5. `experiments/audit_fixes/replay/paper_master_original_backup.pdf` (293,984 bytes) — duplicate backup of baseline.

### B. Blocked Provenance Unclear (5,182 Duplicate Groups & Validation Replay)
1. **5,182 Cross-Year Duplicate Corpus Groups (10,365 physical PDFs):**
   - Year folder dimensions reflect upstream AWS S3 archive partitions.
   - Deletion would destroy exact 39,069-file acquisition counts and construction traceability.
   - Preserved 100% in place.
2. **Four-File Anomaly (1980_2_292_297 vs 1980_2_293_297):**
   - Resolved in Prompt 17 as `DISTINCT_DOCUMENTS_SAME_BYTES` (distinct upstream legal catalog records sharing scanned bytes).
   - Preserved 100% in place.
3. **`validation_replay/` (28 files, 154 MB):**
   - Preserved per explicit owner instructions pending future external provenance review.

---

## 5. Residual Repository State Analysis

- **Caches:**
  - `artifacts/e2_hf_cache/` (1.08 GB) & `experiments/audit_fixes/replay/e2_hf_cache/` (1.08 GB): Maintained for active HuggingFace offline model evaluation.
  - `experiments/audit_fixes/replay/e2_cache/` (154 MB): Precomputed evaluation pooling representations.
- **Audit Evidence:**
  - `corpus_consolidation_manifest.json` (1.68 KB) & `artifacts/local_cleanup/local_cleanup_manifest.json` (839 KB): Uniquely record historical cleanup operations.
  - `experiments/audit_fixes/replay/project_cleanup_scan/`: Contains all complete, phase-by-phase audit logs, manifests, and integrity checks (Prompts 14–19).
- **Build Outputs:**
  - `demo/web/dist/` (150 KB): Preserved as `REGENERABLE_BUT_KEEP_FOR_NOW` to facilitate immediate local demo execution without requiring npm rebuilds.
- **Secrets:**
  - **Zero** plaintext credentials, secrets, or connection strings remain anywhere in the repository.
  - `.gitignore` continues to enforce strict ignore patterns (`.env`, `.db_env`, `*.key`, etc.).

---

## 6. Top 5 Largest Residual Storage Consumers

1. `corpus/` — 23.81 GB (Raw judicial PDFs and yearly metadata partitions)
2. `experiments/` — 3.54 GB (Audit replays, reproduction logs, and replay model caches)
3. `retrieval/` — 2.27 GB (`bm25.sqlite` search index)
4. `artifacts/` — 1.52 GB (Frozen checkpoints, evaluation JSONs, and HF cache)
5. `validation_replay/` — 0.15 GB (Historical validation cache)
