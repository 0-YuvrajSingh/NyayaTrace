# CLAUDE.md — NyayaTrace

Quick-orientation guide. Read this first; open other files only when a task needs them.

## What this project is
**NyayaTrace** is a research prototype (paper: *"Temporally Constrained, Provenance-Verified Evidence Retrieval for Indian Legal Research"*) for **auditable, evidence-backed legal research over historical Indian Supreme Court judgments**. It is NOT automated adjudication or legal advice. The project is at the **final paper/submission stage** — most work now is auditing, reproducibility, and manuscript edits, not new modelling.

Core ideas:
- **Temporal integrity**: when researching a query case from year Y, only precedents decided **strictly before Y** are eligible (same year = ambiguous → excluded; missing date → excluded). The filter is applied **before** BM25 ranking/LIMIT (pre-rank), not after.
- **Provenance**: every evidence passage traces back to source PDF, page, citation, decision date (stored in PostgreSQL).
- **Verification**: citations, provenance, duplicates/self-matches, grounding, and temporal eligibility are checked explicitly.
- **Frozen & reproducible**: configs, answer key, index, and checkpoint are frozen and hash-checked (`config/reproducibility_freeze.json`). Never silently change frozen artifacts or reported numbers.

## Source hierarchy (when sources conflict)
1. **Canonical spec** ("Indian_Legal_XAI", Document 3), the sole source of truth for scope; controlled copy `docs/INDIAN_LEGAL_XAI.docx` ("Fixed Project Scope — Controlled Copy"). It allows no new RQs, experiments, datasets, metrics, models or technologies. The paper's narrower focus is recorded separately in `docs/PAPER_SCOPE_DECISION.md` and does not change the project scope.
2. Repository artifacts: what was actually built, frozen and measured.
3. `submission/research_paper.tex` is the one canonical manuscript (no copies elsewhere).
4. The compiled PDF.
5. Reviewer comments are suggestions, not requirements.

When sources conflict, name the conflict and classify it (scope / implementation / manuscript / reviewer). Never invent a resolution, and never make evidence fit the wording.

## Canonical spec essentials
- **Primary task:** legal research with evidence-backed case analysis (retrieve → select → verify citations and provenance → structured explanation). **Secondary:** outcome prediction. Humans review every output.
- **Canonical RQs:** RQ1 asks whether evidence grounding beats a facts-only legal-language baseline on reliability and retrieval. RQ2 asks whether provenance constraints and verification reduce unsupported claims (H2: compared with an unconstrained condition). RQ3 asks whether a structured explanation improves human-verifiable transparency without hurting performance (human-rated).
- **Temporal eligibility is an integrity control, NOT the novelty claim.** The canonical rule is `decision_date <= case_date`. The implementation uses `decision_year < query_year` because ILDC dates are year-only. This is a deviation and must be named, never treated as equivalent.
- **Canonical metrics:** Recall@k, Authority-consistency P/R/F1, Citation Groundedness Rate, Citation Provenance Validity, **Temporal Violation Rate (the only required temporal metric)**, Unsupported-claim rate, human explanation quality, Acc/Macro-F1, efficiency. FEER/FCER and other temporal sub-metrics are not frozen deliverables.
- **Non-goals:** AI judge or advisor, multilingual support, GraphRAG or graph databases, agents, leaderboard model zoos. Never equate provenance with legal correctness, or confidence with certainty.
- **Mandatory error analysis:** E2✗/E3✓; E3✓/E4✗; prediction ✓ with an unsupported citation; right authority but wrong answer; traceable but authority-inconsistent; post-dated citation; unfaithful explanation.

## Paper vs project (most important rule)
The six-page IEEE paper is a **deliberately narrowed slice**: corpus alignment, temporal-constrained BM25, provenance and citation verification, authority recovery, and secondary prediction. RQ3, human evaluation, generation and the demo are deferred. Do not mark the paper "wrong" for omitting broader-scope items. Do check that it says it is narrowed.
- **Not implemented anywhere:** controlled generation (`generation_mode: controlled_extract_only`), attribution analysis, statute-validity metadata, efficiency metrics.
- **Exists but not in the paper:** a 37-case extension (`answer_key/extension_v6`, `experiments/rq1|rq2`), RQ2 positive controls (111/111 mutations rejected), and an exploratory **LLM-judge** RQ3 (`experiments/rq3`, 4 LLMs × 14 cases). The LLM-judge study is not human evaluation.
- **Paper status (2026-10-09):** canonical source `submission/research_paper.tex` → `submission/research_paper.pdf` (6 pages). Validate with `python validate_final.py` (needs `pymupdf` or `pypdf`; cross-checks numbers against frozen artifacts and recomputes the freeze audit). Build with `./tectonic.exe -X compile submission/research_paper.tex --outdir submission`. No DOCX. Plots in `submission/figures/` are regenerated by `scripts/build_week14_paper_figures.py`. Template: `\documentclass[conference]{IEEEtran}` with template-default spacing; `\usepackage[T1]{fontenc}` is required so Tectonic's XeTeX engine sets the text in Times (without it the PDF silently falls back to Latin Modern). Do not reintroduce `\resizebox` tables or spacing overrides.
- **Final RQ1 verdict:** `docs/RQ1_FINAL_ADJUDICATION.md`. Rebuilt read-only from the frozen index; 30/30 cases match the artifacts. Recall@5 (selected) is 11/30 → 12/30; R@100 is 12/30 → 15/30. The direction is guaranteed by construction. Base-30 informed both the query-builder choice (6 cases) and the pre-ranking adoption. Status: development-informed, exploratory systems characterisation.
- **Authoritative verified findings:** `docs/GROUND_TRUTH_ADJUDICATION.md` (non-RQ1) and `docs/RQ1_FINAL_ADJUDICATION.md`. Key traps:
  - The RQ1 "unfiltered" baseline is really a **post-ranking filter** (`artifacts/week11_initial_evaluation.json`).
  - Code's `recall_at_5` = raw rank ≤5. The paper defines it as "selected among 5"; under that definition the baseline is 11/30, not 5/30.
  - Pre-ranking was adopted after the 30-case **test** comparison.
  - Freeze: 39 paths = 29 exact / 8 line-ending-only / 2 changed (`docs/freeze_drift_audit.md`, corrected 2026-10-09).
  - Tests: 81/81 pass — 75 on the host; the 6 torch/transformers tests in Docker image `nyayatrace-e2:frozen` (2026-10-09, `experiments/audit_fixes/replay/logs/pytest_docker_2026-10-09.log`).
  - Git history starts 2026-09-12, so earlier chronology comes only from timestamps inside the artifacts.
  - The default Python 3.14 lacks project deps. Use a scratch venv to run tests.

## Data
- **ILDC Single** (`corpus/ildc/`, parquet, HF `Exploration-Lab/IL-TUR`): query cases with outcome labels. Splits train 5082 / val 994 / test 1517. Year-only dates.
- **eCourts SC judgments 1950–2020** (`corpus/ecourts/`): evidence corpus, 39,069 PDFs → ~2.34M cleaned page-bound chunks. Indexed in BM25 (`retrieval/bm25.sqlite`, SQLite FTS) with provenance in PostgreSQL.
- ILDC IDs look like eCourts `YYYY INSC N` IDs but are **not** the same namespace — identity mapping requires content/title alignment (`alignment.py`).
- **Answer key** (`answer_key/`): manually verified expected authorities per test case. Frozen 30-case subset for E3/E4; later expansions in `expansion_v5/`, `extension_v6/` (37-case runs in `experiments/rq1|rq2`).
- Large assets (corpus, index, checkpoints, HF cache) are git-ignored, local only.

## Experiments (E1–E4)
| Exp | What | Notes |
|---|---|---|
| E1 | TF-IDF + Logistic Regression on facts-only text | test acc 0.6134 / macro-F1 0.6123 |
| E2 | InLegalBERT (`law-ai/InLegalBERT`) chunk-and-pool, 512 tok windows, 50 overlap, mean logits | acc 0.5968 / F1 0.5924. Checkpoint `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318`. Old 256-token result discarded (truncation bug). |
| E3 | Retrieval + grounded evidence brief + outcome prediction | Prediction = **frozen E2 checkpoint**, input = facts + selected evidence (inference-only, no training) |
| E4 | E3 + citation/provenance/temporal verification (reliability constraints) | E3 & E4 both acc 0.666667 / F1 0.603175 on 30-case subset |

Facts-only input (`facts.py`, rule `ildc-predecision-facts-v1`): keep text before the earliest dispositive cue — shared by E1/E2/E3/E4.
FEER/FCER metrics were **removed** on mentor guidance; temporal integrity reported via eligibility/violation counts.

Research questions: RQ1 (retrieval/authority recall), RQ2 (temporal/verification), RQ3 (explanation presentation: structured vs unstructured, human evaluator packet) — see `experiments/rq*/`.

## Pipeline (E3/E4)
```
ILDC case → facts.py (pre-decision facts)
  → retrieval.py: salient TF-IDF query terms (≤32)
  → evidence_pipeline.py: BM25 top-100 with temporal pre-rank filter (temporal.py)
      → exclude self/duplicate matches (≥100 shared 6-grams & ≥80% fingerprint overlap)
      → select_diverse_evidence: ≤5 passages, max 1 chunk per source
  → grounded_answer.py: extract-only brief (no generation, verbatim passages + provenance)
  → citation_verifier.py: citation/metadata/temporal checks vs corpus & answer key
  → evidence_augmented_prediction.py: E2 checkpoint on facts + evidence → outcome
```
Selection version: `week11-bm25-salient-terms-preranked-temporal-v3` (`config/evidence_selection.json`).

## Repository map
- `src/legal_xai/` — core library (≈10 small modules, listed above + `corpus.py` chunking/cleaning, `answer_key.py` split enforcement, `alignment.py` ILDC↔eCourts identity).
- `scripts/` — CLI entry points: build index/corpus, train E1/E2, run evaluations/replays, audits, figures. Names often carry a "weekN" prefix from the project timeline (weeks 7–16).
- `config/` — frozen JSON configs per experiment; `reproducibility_freeze.json` is the master record.
- `tests/` — pytest unit tests for each `src` module (`pytest.ini`: `pythonpath = src`).
- `artifacts/` — results (JSON/MD), audits, figures, model checkpoints/caches. Source of truth for reported numbers.
- `experiments/` — RQ1–RQ3 runs/reports; `audit_fixes/` = many one-off audit/rebuild scripts from the final audit pass.
- `answer_key/`, `validation_prep/` (CIs, RQ3 spec), `validation_replay/` (baseline reproduction).
- `demo/` — (1) static viewer (`index.html`, `app.mjs`) of precomputed Week 13 cases; (2) connected stack: React `demo/web` → Spring Boot `demo/spring-api` → FastAPI `demo/ml-service` over the unchanged pipeline. Loopback only, not production.
- `submission/` — canonical paper (`research_paper.tex/.pdf`), evaluation plots (`figures/`), MANIFEST, templates. `tectonic.exe` at the root is the local (git-ignored) TeX engine.
- `docs/` — adjudications, freeze audit, hash erratum, repository audit, cleanup record (`docs/REPOSITORY_CLEANUP_2026-10-09.md` lists every file removed and why).
- Root: README, CLAUDE.md, `validate_final.py`, chronology (`PROJECT_CHECKLIST.md`), baseline-reproduction and validation-prep records, transfer manifest, `all_40_corrections_full.txt` (historical reviewer instructions; origin of the retracted 30/22/8 sentence).

## Common commands (Windows / PowerShell)
```powershell
python -m pip install -r requirements.txt
pytest                                            # unit tests
python scripts/serve_week16_demo.py --port 8000   # static demo → http://127.0.0.1:8000/demo/
docker compose -f compose.demo.yaml up --build    # connected demo stack
docker compose up -d                              # PostgreSQL provenance DB (needs POSTGRES_PASSWORD), port 54329
$env:LEGAL_XAI_DATABASE_URL = "postgresql://legal_xai:<password>@127.0.0.1:54329/legal_xai"  # required by DB-backed scripts
$env:PYTHONPATH = "src;scripts"; python scripts/run_e3_e4_evidence_augmented_evaluation.py --force
python scripts/run_week10_reproducibility_replay.py
```
Full replays need local corpus, BM25 index, PostgreSQL, and the cached E2 checkpoint (GPU for prediction).

## Working rules
- **Paper edits:** make targeted edits only. Preserve frozen numbers unless an artifact proves an error. Keep negative results and limitations. Make no unsupported novelty claims. Keep the six-page limit. Don't "humanize" text or optimize it for AI detectors. Don't invent experiments, annotations, citations or causal stories. When proposing an edit, show the current wording, the proposed wording, the reason, and its impact (scope/experiment/claim/style).
- `validate_final.py` asserts specific corrected sentences and the absence of stale claims in the .tex. Update it whenever you change those sentences.
- Don't retrain/modify E1/E2 or the checkpoint; E3/E4 reuse it unchanged.
- Don't alter frozen configs, answer keys, or reported metrics without an explicit request; changes require an audit/erratum trail (see `docs/`).
- Never commit corpora, indexes, checkpoints, or credentials (`.env`) — see `.gitignore`. No credential may be hardcoded; use `LEGAL_XAI_DATABASE_URL`. The old DB password (the former hardcoded default; value withheld) and demo value (the former documented demo value; withheld) remain in git history and must be treated as compromised.
- Preserve verbatim passage text (including OCR errors); the explanation layer is extract-only.
- Branch in use: `audit-fixes` (also `main`, `paper-submission-v1-prep`; tags up to `v6-final-publication`).
