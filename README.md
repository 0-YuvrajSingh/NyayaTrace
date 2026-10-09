# Temporally Constrained and Provenance-Verified Legal Research

This repository contains a research prototype for auditable legal research over historical Indian Supreme Court judgments. E1/E2 provide facts-only outcome baselines. E3/E4 retrieve and verify evidence and also emit outcome predictions by reusing the frozen E2 InLegalBERT checkpoint with inference-time evidence augmentation. The system preserves source identity, passage locations, decision dates, retrieval configuration, prediction metadata, and evaluation outputs so that reported results can be inspected and replayed.

## Purpose and scope

The project is designed for evidence-backed legal research, not automated adjudication or legal advice. It includes:

- facts-only outcome baselines using TF-IDF/logistic regression and InLegalBERT chunk-and-pool;
- temporally constrained BM25 retrieval with source-diverse evidence selection;
- evidence-augmented E3/E4 outcome prediction using the unchanged E2 checkpoint;
- exact citation, provenance, duplicate, grounding, and temporal verification; and
- a static researcher-facing interface for inspecting precomputed evidence briefs.

The interface does not provide accounts, multi-user services, arbitrary live retrieval, or a production database backend.

## Installation

Install the pinned Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

The reproducibility record specifies the required local corpus, database, index, and model assets. Large assets are intentionally excluded from version control; their hashes and availability requirements are recorded in [`config/reproducibility_freeze.json`](config/reproducibility_freeze.json).

## Run the demonstration interface

The demonstration interface reads precomputed artifacts and does not run retrieval on demand:

```powershell
python scripts/serve_week16_demo.py --port 8000
```

Open <http://127.0.0.1:8000/demo/> while the server is running. It includes representative clean-success, near-miss, authority-consistency, and absent-at-k=100 cases. Detailed verification instructions are in [`demo/README.md`](demo/README.md).

A connected local research stack (React + Spring Boot + FastAPI over the frozen pipeline) is also available via `docker compose -f compose.demo.yaml up --build`; see [`demo/README.md`](demo/README.md). It is loopback-only and not production.

## Reproduce the evaluation

The replay contract and required environment are documented in [`config/reproducibility_freeze.json`](config/reproducibility_freeze.json) and [`artifacts/week16_reproducibility_audit.md`](artifacts/week16_reproducibility_audit.md). With the hash-checked ILDC files, eCourts/PostgreSQL provenance store, BM25 index, and locally cached E2 checkpoint available, run:

```powershell
python scripts/run_week10_reproducibility_replay.py
```

The replay compares independent E4 runs after excluding generated retrieval-run UUIDs. To reproduce the later E3/E4 evidence-augmented prediction evaluation on the frozen 30-case subset, with the existing provenance database running, use:

```powershell
$env:PYTHONPATH = "src;scripts"
python scripts/run_e3_e4_evidence_augmented_evaluation.py --force
```

This command reuses local checkpoint-6318 and does not train or modify E1/E2. Credentials are never stored in the repository: start PostgreSQL with `POSTGRES_PASSWORD` set (see [`compose.yaml`](compose.yaml)) and give every database-backed script the connection string through `LEGAL_XAI_DATABASE_URL` (scripts exit if it is unset).

## Data sources and licences

| Asset | Source | Licence | In this repository |
| --- | --- | --- | --- |
| eCourts Supreme Court judgments (1950–2020) | [Indian Supreme Court Judgments](https://registry.opendata.aws/indian-supreme-court-judgments) (Dattam Labs, AWS Open Data; acquired 2026-08-27) | CC BY 4.0 | Raw PDFs/metadata and cleaned chunks are local only (`corpus/ecourts/`, git-ignored); identity hashes in `artifacts/ecourts_corpus_identity.json` |
| ILDC Single splits | `Exploration-Lab/IL-TUR` on Hugging Face (revision in `config/datasets.json`) | CC BY-NC-SA 4.0 (the frozen `corpus/dataset_manifest.md` records the original CJPE repository's CC BY-NC) | Parquet files local only (`corpus/ildc/`, git-ignored). Derived excerpts in tracked artifacts (e.g. review packets) remain under the same non-commercial, share-alike terms |
| InLegalBERT | `law-ai/InLegalBERT` (revision in `config/e2_chunk_pool.json`) | MIT | Weights and checkpoint local only |

Reconstruct the corpus with `scripts/download_dual_corpus.py` / `scripts/acquire_ecourts_pdfs.py`, then verify it against `config/reproducibility_freeze.json`.

## Evaluation revision

Outcome prediction was added to E3/E4 in a later revision, extending the original evidence-only implementation by reusing the E2 checkpoint through inference-time evidence augmentation. On the frozen 30-case answer-key subset, both E3 and E4 achieved accuracy 0.666667 and macro-F1 0.603175. FEER and FCER were removed from the reported metrics on the project mentor's guidance; temporal integrity continues to be reported through direct eligibility and violation counts.

## Repository guide

- **Project scope:** [`docs/INDIAN_LEGAL_XAI.docx`](docs/INDIAN_LEGAL_XAI.docx), the canonical specification (Document 3, Final) as a fixed-scope controlled copy. The paper's narrower focus is recorded in [`docs/PAPER_SCOPE_DECISION.md`](docs/PAPER_SCOPE_DECISION.md) and does not change the project scope.
- **Submission package:** [`submission/`](submission/) — see [`submission/README.md`](submission/README.md).
- **Canonical paper:** [`submission/research_paper.tex`](submission/research_paper.tex) → [`submission/research_paper.pdf`](submission/research_paper.pdf) (six-page IEEEtran). Build with Tectonic 0.15.0 (`tectonic -X compile submission/research_paper.tex --outdir submission`; the binary is local and git-ignored) and validate with `python validate_final.py` (needs `pymupdf` or `pypdf`), which checks every reported number against the frozen artifacts.
- **Evaluation plots:** [`submission/figures/`](submission/figures/), regenerated by `python scripts/build_week14_paper_figures.py` from [`artifacts/week14_results_evidence_inventory.json`](artifacts/week14_results_evidence_inventory.json).
- **Scientific adjudication:** [`docs/RQ1_FINAL_ADJUDICATION.md`](docs/RQ1_FINAL_ADJUDICATION.md) (verified Recall@5/Recall@100, the post-ranking control, why the Base-30 temporal comparison is exploratory) and [`docs/GROUND_TRUTH_ADJUDICATION.md`](docs/GROUND_TRUTH_ADJUDICATION.md) (freeze audit, leakage, E1/E2 data, tests, references).
- **Reproducibility configuration:** [`config/reproducibility_freeze.json`](config/reproducibility_freeze.json); freeze audit [`docs/freeze_drift_audit.md`](docs/freeze_drift_audit.md); hash erratum [`docs/FROZEN_MANIFEST_ERRATUM.md`](docs/FROZEN_MANIFEST_ERRATUM.md).
- **Evaluation and replay audits:** [`artifacts/week16_reproducibility_audit.md`](artifacts/week16_reproducibility_audit.md); independent reproduction in [`validation_replay/`](validation_replay/) ([`FINAL_BASELINE_REPRODUCTION.md`](FINAL_BASELINE_REPRODUCTION.md)); audit-fix replay, temporal erratum, answer-key replacement and leakage audits in [`experiments/audit_fixes/`](experiments/audit_fixes/).
- **Experiment evidence:** weekly QA, investigations, and frozen results in [`artifacts/`](artifacts/); answer key and extension in [`answer_key/`](answer_key/); RQ1–RQ3 37-case runs in [`experiments/rq1`](experiments/rq1), [`rq2`](experiments/rq2), [`rq3`](experiments/rq3).
- **Chronology:** [`PROJECT_CHECKLIST.md`](PROJECT_CHECKLIST.md) (week-by-week); repository cleanup record [`docs/REPOSITORY_CLEANUP_2026-10-09.md`](docs/REPOSITORY_CLEANUP_2026-10-09.md).
- **Evidence-augmented prediction:** [`config/e3_e4_evidence_augmented_prediction.json`](config/e3_e4_evidence_augmented_prediction.json), [`artifacts/e3_e4_evidence_augmented_evaluation.json`](artifacts/e3_e4_evidence_augmented_evaluation.json), and [`artifacts/e3_e4_prediction_error_analysis.md`](artifacts/e3_e4_prediction_error_analysis.md).
- **Source modules and scripts:** [`src/legal_xai/`](src/legal_xai/) and [`scripts/`](scripts/).
- **Demonstration interface:** [`demo/`](demo/).

The repository includes the E1-E4 implementations, retrieval-index build record, citation and provenance modules, the extract-only explanation renderer, evaluation outputs and plots, error-analysis reports, reproducibility records, demonstration interface, and paper source. The curated index and model checkpoints remain local artifacts by design and are verified through their recorded hashes. Institutional declaration and certificate templates are included as neutral placeholders where no institution-specific template was supplied.
