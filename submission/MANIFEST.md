# Required-deliverable manifest

| Required deliverable | Included location | Status / note |
| --- | --- | --- |
| E1 outcome-prediction implementation | `../scripts/train_e1_baseline.py`, `../scripts/reconstruct_e1_predictions.py`, `../src/legal_xai/` | Included in source tree; frozen config and results are tracked. |
| E2 outcome-prediction implementation | `../scripts/train_e2_chunk_pool_cached.py`, `../scripts/infer_e2_checkpoint_predictions.py`, `../config/e2_chunk_pool.json` | Included; checkpoint weights remain locally cached by design and are hash-recorded in the freeze. |
| E3 retrieval and evidence-selection implementation | `../src/legal_xai/retrieval.py`, `../src/legal_xai/evidence_pipeline.py`, `../scripts/run_evidence_pipeline.py` | Included; final selection configuration is frozen. |
| E4 citation/provenance verification implementation | `../src/legal_xai/citation_verifier.py`, `../src/legal_xai/grounded_answer.py`, `../scripts/run_grounded_answer_pipeline.py` | Included; exact passage, provenance, duplicate, and temporal checks are tracked. |
| Curated retrieval index | `../retrieval/bm25.sqlite` (local), `../artifacts/bm25_index.json` (tracked build record) | The multi-gigabyte SQLite index is gitignored; its hash and build record are frozen. |
| Citation/provenance module | `../src/legal_xai/citation_verifier.py`, `../scripts/load_provenance.py`, `../config/citation_verification.json` | Included. |
| Explainability module | `../src/legal_xai/grounded_answer.py`, `../demo/` | Included; static frozen-artifact viewer plus connected React/Spring/FastAPI local demo (see `../demo/README.md`). |
| Evaluation tables and plots | `../artifacts/e1_e2_comparison.*`, `../artifacts/week11_temporal_prerank_evaluation.json`, `figures/` | Included; `figures/` holds report figures not embedded in the six-page paper. Regenerated 2026-10-09 by `../scripts/build_week14_paper_figures.py` with the adjudicated RQ1 framing; captions in `figures/captions.md`. |
| Error-analysis report | `../artifacts/week12_error_analysis.md`, `../artifacts/e3_e4_prediction_error_analysis.md`, `../docs/GROUND_TRUTH_ADJUDICATION.md` (leakage, E1/E2 asymmetry) | Included. |
| Reproducibility configuration and manifest | `../config/reproducibility_freeze.json`, `../artifacts/week16_reproducibility_audit.md` | Freeze audit (2026-10-09): of 39 hashed paths, 29 byte-identical, 8 line-ending-only, 2 record files without reported metrics changed in content (`../docs/freeze_drift_audit.md`). |
| Minimal demo and instructions | `../demo/README.md`, `../scripts/serve_week16_demo.py` | Included; static viewer plus connected stack via `compose.demo.yaml`; local single-user scope, not production. |
| Final paper | `research_paper.pdf`, `research_paper.tex` | Six-page IEEEtran PDF plus LaTeX source; validated by `../validate_final.py`. |
| Presentation/demo script | `../demo/README.md`, `../artifacts/week16_demo.png` | Launch and verification instructions plus reference screenshot included. |
| Declaration/certificate pages | `declaration_template.md`, `certificate_template.md` | Neutral placeholders included because no institutional template was supplied. |
