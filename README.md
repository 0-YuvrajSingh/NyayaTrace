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

This command reuses local checkpoint-6318 and does not train or modify E1/E2. Credentials are supplied through the documented environment-variable mechanism and are not stored in the repository.

## Evaluation revision

Outcome prediction was added to E3/E4 in a later revision, extending the original evidence-only implementation by reusing the E2 checkpoint through inference-time evidence augmentation. On the frozen 30-case answer-key subset, both E3 and E4 achieved accuracy 0.666667 and macro-F1 0.603175. FEER and FCER were removed from the reported metrics on the project mentor's guidance; temporal integrity continues to be reported through direct eligibility and violation counts.

## Repository guide

- **Paper and submission files:** [`submission/`](submission/), including the formatted PDF, editable Markdown source, HTML rendering, figures, and institutional declaration/certificate templates.
- **Current paper source:** [`submission/paper.md`](submission/paper.md). Earlier working drafts remain under [`artifacts/`](artifacts/) for traceability.
- **Reproducibility configuration:** [`config/reproducibility_freeze.json`](config/reproducibility_freeze.json).
- **Evaluation audit:** [`artifacts/week16_reproducibility_audit.md`](artifacts/week16_reproducibility_audit.md).
- **Results and figures:** [`artifacts/`](artifacts/) and [`artifacts/figures/`](artifacts/figures/).
- **Evidence-augmented prediction:** [`config/e3_e4_evidence_augmented_prediction.json`](config/e3_e4_evidence_augmented_prediction.json), [`artifacts/e3_e4_evidence_augmented_evaluation.json`](artifacts/e3_e4_evidence_augmented_evaluation.json), and [`artifacts/e3_e4_prediction_error_analysis.md`](artifacts/e3_e4_prediction_error_analysis.md).
- **Source modules and scripts:** [`src/legal_xai/`](src/legal_xai/) and [`scripts/`](scripts/).
- **Demonstration interface:** [`demo/`](demo/).

The repository includes the E1-E4 implementations, retrieval-index build record, citation and provenance modules, explainability renderer, evaluation outputs and figures, error-analysis reports, reproducibility records, demonstration interface, and paper source. The curated index and model checkpoints remain local artifacts by design and are verified through their recorded hashes. Institutional declaration and certificate templates are included as neutral placeholders where no institution-specific template was supplied.
