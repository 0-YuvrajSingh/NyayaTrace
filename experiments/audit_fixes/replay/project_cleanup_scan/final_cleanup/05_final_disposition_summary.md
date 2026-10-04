# 05 — Final Disposition Summary

Comprehensive disposition summary concluding Prompt 19 and the repository-wide cleanup sequence.

---

## Deleted Safely
Only items actually removed during Prompt 19 execution:
1. `experiments/audit_fixes/replay/.db_env` (132 bytes) — live database credential from completed replay.
2. `paper_master_6page.tex` (31,746 bytes) — obsolete alternate manuscript variant.
3. `paper_master_6page.pdf` (222,823 bytes) — obsolete compiled PDF of 6page variant.
4. `artifacts/figures/week14_figure_a_outcome_prediction.svg` (5,938 bytes) — redundant duplicate figure.
5. `artifacts/figures/week14_figure_b_retrieval_funnel.svg` (2,723 bytes) — redundant duplicate figure.
6. `artifacts/figures/week14_figure_c_retrieval_investigation.svg` (8,354 bytes) — redundant duplicate figure.
7. `artifacts/figures/week14_figure_d_integrity_summary.svg` (4,017 bytes) — redundant duplicate figure.
8. `artifacts/figures/week14_figure_e_explanation_review.svg` (5,916 bytes) — redundant duplicate figure.
*(Total removed: 8 files, 281,649 bytes; empty directory `artifacts/figures` deleted).*

---

## Preserved Canonical
Authoritative canonical files:
- **Canonical Manuscript:** `paper_master_final.tex` and `paper_master_final.pdf` (authoritative 6-page camera-ready manuscript).
- **Canonical Figures:** `figures/fig1_outcome.pdf` through `fig5_explanation.pdf` and `submission/figures/*.svg`.
- **Model Checkpoint:** `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/model.safetensors` (437.96 MB).
- **Search Index:** `retrieval/bm25.sqlite` (2.27 GB).
- **Configuration & Code:** `compose.yaml`, `compose.demo.yaml`, `requirements.txt`, `.gitignore`, `scripts/`, `src/`.

---

## Preserved Audit Evidence
Essential verification artifacts:
- **Audit Baseline Manuscript:** `paper_master.tex` and `paper_master.pdf` (tracked original baseline).
- **Replay & Audit Manifests:** `corpus_consolidation_manifest.json`, `artifacts/local_cleanup/local_cleanup_manifest.json`.
- **Evaluation Outputs:** `artifacts/e2_chunk_pool_results.json`, `artifacts/e3_e4_evidence_augmented_evaluation.json`, `experiments/audit_fixes/replay/e3e4_replay.json`.
- **Complete Audit Trail:** `experiments/audit_fixes/replay/project_cleanup_scan/` (Prompts 14–19 audits).

---

## Preserved Provenance
Corpus and provenance assets:
- **Corpus Judicial PDFs:** 39,068 files in `corpus/ecourts/pdfs/` (preserving all per-year source partitions).
- **Metadata Parquets:** 74 files in `corpus/` (71 yearly partitions in `ecourts/metadata/` + 3 ILDC splits).
- **Corpus Cleaning & Acquisition Records:** `acquisition_record.json`, `cleaning_record.json`, `chunks.jsonl`.
- **Ground Truth:** `answer_key/authority_answer_key.json` (30 verified ground-truth cases).

---

## Blocked Pending Owner Decision
Items requiring future owner determination:
- **`validation_replay/` (28 files, 154 MB):** Preserved per explicit owner instructions pending future decision on independent replay data.
- **5,182 Cross-Year Duplicate Groups (10,365 PDFs):** Preserved because folder partitions mirror upstream archive structure and deletion alters corpus construction counts.

---

## Blocked Pending Archive Destination
Obsolete files that must not be deleted and cannot be archived until an approved archive structure exists:
1. `paper_master_revised.tex` (56,898 bytes) — superseded manuscript draft.
2. `paper_master_revised.pdf` (294,801 bytes) — compiled PDF of superseded draft.
3. `Indian_Legal_XAI.docx` (27,166 bytes) — obsolete initial proposal/spec.
4. `experiments/audit_fixes/replay/paper_master_original_backup.tex` (55,994 bytes) — duplicate backup of baseline.
5. `experiments/audit_fixes/replay/paper_master_original_backup.pdf` (293,984 bytes) — duplicate backup of baseline.

---

## Remaining Cleanup Opportunities
- Archiving the 5 blocked files above into an approved archival directory once designated by the owner.
- Archival or cleanup of `validation_replay/` once external reproduction validation is confirmed complete.
- Stale Docker builder cache reclamation (host-level command: `docker builder prune`).

---

## Corpus Status
- **Cross-Year Groups Remaining:** 5,182 groups (10,365 physical files) — 100% preserved.
- **Four-File Anomaly Status:** Preserved in place under classification `DISTINCT_DOCUMENTS_SAME_BYTES` (two distinct upstream catalog entries sharing scanned bytes).
- **Corpus Mutation Status:** **ZERO MUTATION**. Zero corpus PDFs or parquets were modified, renamed, or deleted.

---

## Reproducibility Status
- **Model Checkpoint:** Intact and bit-identical (SHA-256: `924A5BB9078BCC212EF07ACB9F08DFAA8593E880AE3868203DEB28586DBDC773`).
- **E2 Cache:** `experiments/audit_fixes/replay/e2_cache/` intact.
- **HuggingFace Cache:** `artifacts/e2_hf_cache/` and `experiments/audit_fixes/replay/e2_hf_cache/` intact.
- **Frozen Results:** `e2_chunk_pool_results.json`, `e3_e4_evidence_augmented_evaluation.json`, `e3e4_replay.json` intact.
- **BM25 Index:** `retrieval/bm25.sqlite` intact and bit-identical (SHA-256: `3187F7FCE824EA8CCC5A26D908936CE4B78E81238289EA69348CB861350D65FB`).
- **Configs & Scripts:** All 65 pipeline scripts in `scripts/`, `src/`, and `config/` intact. Unit tests pass.

---

## Final Integrity

### **`PASS`**
