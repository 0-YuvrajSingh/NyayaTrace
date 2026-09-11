# NyayaTrace — Final Baseline Audit (read-only, current-state as of 2026-09-11)

> Method: static inspection + physical existence checks only. No files modified, no experiments rerun, no models retrained, no indexes rebuilt, no datasets downloaded, no large dependencies installed. Test suite was executed read-only (`pytest`) solely to record current state. Secrets are reported as YES/NO + location only; no values printed. Uncertain items are marked UNKNOWN with missing evidence noted.
> Audit date (UTC): 2026-09-11. Working directory: `C:\Users\uvi58\OneDrive\Documents\NyayaTrace`.

---

## 1. Executive Summary

NyayaTrace is a research prototype for **auditable legal research over historical Indian Supreme Court judgments**, not automated adjudication or legal advice (`README.md:7`). The implemented system links two corpora (ILDC Single for outcome baselines; eCourts-derived evidence corpus for retrieval), applies a frozen pre-decision facts extractor, temporally constrained BM25 retrieval with source-diverse evidence selection, an extract-only explanation renderer, and an exact citation/provenance/duplicate/temporal verifier, with a static precomputed demo.

Physically verified baseline: ~39,530 files (39,070 PDFs); ILDC splits present (5,082 / 994 / 1,517 = 7,593 rows); eCourts cleaned chunks present (71 year dirs); BM25 SQLite index present (2,269,376,512 bytes); E2 checkpoint-6318 present; E1/E2/E3/E4 result artifacts present and frozen at `final-reproducibility-freeze-v4-e3e4-prediction`; answer key = **30 evaluation + 3 dev_example = 33 entries** (target 40, NOT 75/100); human evaluation = **author self-review fallback on 7 cases, not independent review**; tests = **75 passed, 2 collection errors** (missing `torch`/`transformers` on host); PostgreSQL/Docker **not running in this audit environment** (service-unavailable, not asset-missing); git working copy has **no commits** (transfer copy, history absent).

The strongest completed claims (all frozen, reproduced per `artifacts/week16_reproducibility_audit.json`): E1 test acc 0.6134 / macro-F1 0.6123 (N=1503); corrected E2 mean-logit acc 0.5968 / F1 0.5924 (N=1503); E3=E4 retrieval Recall@5 0.40 (12/30), Recall@100 0.50 (15/30), 150/150 citations grounded + provenance-valid + temporally eligible, 0 violations, 0 unsupported; E3=E4 evidence-augmented prediction acc 0.6667 / F1 0.6032 (N=30, small sample, no CI). The discarded 256-token E2 run (acc 0.5695) is retained for traceability only. Recovery remains the binding constraint (15/30 absent at k=100); answer-key size/era balance (n=30, 43% 1980s), single-authority-per-case coverage, independent human evaluation, and 75–100-case extension are the explicit deferred items (`submission/paper.md:327`).

---

## 2. Repository Inventory

Top-level entries (verified `read` of root): `.git/ .gitattributes .gitignore answer_key/ artifacts/ compose.yaml config/ corpus/ demo/ docker/ PROJECT_CHECKLIST.md pytest.ini README.md requirements.txt retrieval/ scripts/ src/ submission/ tests/ TRANSFER_MANIFEST.json TRANSFER_README.md` (21 entries).

File counts (measured `Get-ChildItem -Recurse`): **39,530 files total**. Extension breakdown: `.pdf` 39,070; `.json` 113; `.py` 84; `.parquet` 74 (71 metadata + 3 ILDC); `.md` 73; `.jsonl` 71; `.svg` 10; `.lock` 6; `.mjs` 4; plus singletons (`.sqlite` 1, `.joblib` 1, `.bin` 1, `.safetensors` 2 blobs counted under no-extension/hub layout, `.csv` 1, `.yaml` 1, `.ini` 1, etc.).

Directory sizes (summed file lengths):
- `artifacts/`: ~1,514,450,811 bytes (~1.4 GB incl. HF cache + checkpoint-6318)
- `corpus/`: ~23,810,102,629 bytes (~22.2 GB; dominated by 39,069 PDFs ~21.0 GB + cleaned chunks ~2.7 GB)
- `retrieval/`: ~2,269,376,512 bytes (single `bm25.sqlite`, 2.27 GB)
- `scripts/`, `src/`, `tests/`, `config/`, `demo/`, `submission/`, `answer_key/`: each < 70 KB–530 KB except `submission/paper.pdf` (386,292 B).

Important-file table (PATH | TYPE | PURPOSE | RELATED EXP | STATUS | NOTES):

| PATH | TYPE | PURPOSE | EXP | STATUS | NOTES |
|---|---|---|---|---|---|
| `src/legal_xai/*.py` (10 modules + `__init__.py`) | source | pipeline implementation | E1–E4 | implemented, unit-tested | stdlib-only except retrieval (sklearn), evidence_augmented_prediction (torch/transformers), evidence_pipeline (sqlite/psycopg/pyarrow) |
| `scripts/train_e1_baseline.py` | script | E1 training | E1 | implemented, frozen | TF-IDF+LogReg, C selected on val |
| `scripts/train_e2_baseline.py` | script | discarded 256-prefix E2 | E2-superseded | implemented, discarded | truncation bug documented |
| `scripts/train_e2_chunk_pool_cached.py` + `prepare_e2_chunk_pool_cache.py` + `infer_e2_checkpoint_predictions.py` | scripts | canonical E2 | E2 | implemented, frozen | ckpt-6318 |
| `scripts/run_e3_e4_evidence_augmented_evaluation.py` + `replay_e3_e4_evidence_augmented_evaluation.py` | scripts | E3/E4 eval + replay | E3/E4 | implemented, frozen | parity-enforced E3==E4 |
| `scripts/run_evidence_pipeline.py`, `run_grounded_answer_pipeline.py`, `retrieve_evidence.py`, `verify_citations.py` | scripts | E3/E4 pipelines | E3/E4 | implemented | thin wrappers over `src/` |
| `scripts/build_bm25_index.py`, `load_provenance.py` | scripts | index/DB build | retrieval | implemented | require Postgres + corpus; not rerun in audit |
| `scripts/serve_week16_demo.py` | script | static demo server | demo | implemented | allowlist-only, loopback |
| `scripts/build_reproducibility_freeze.py`, `run_week10_reproducibility_replay.py` | scripts | freeze + replay | repro | implemented | deterministic |
| 60+ `scripts/*.py` (acquire/audit/analyze/build/check/compare/validate/verify/week*) | scripts | staged weekly workflow | all | implemented | headers bounded to frozen QA; no agent/SaaS |
| `tests/test_*.py` (11 files) | tests | unit contracts | all | implemented; 75 pass, 2 collection errors on host | torch/transformers missing on host |
| `config/*.json` (16 files) | config | frozen experiment configs | all | implemented, frozen | IDs listed in §4-arch/§9-12 |
| `compose.yaml` | compose | Postgres 16-alpine, 127.0.0.1:54329 | retrieval/DB | implemented, service not running here | password via env guard |
| `docker/Dockerfile.ocr`, `docker/e2.Dockerfile` | docker | OCR + E2 training images | corpus/E2 | implemented | pins in §8 |
| `corpus/ildc/single_{train,validation,test}.parquet` | dataset | ILDC Single splits | E1/E2 | present, verified sizes | 56/11/17 MB; gitignored |
| `corpus/ecourts/pdfs/year=*/` (39,069 PDFs) | dataset-raw | eCourts source PDFs | E3/E4 | present | ~21 GB |
| `corpus/ecourts/cleaned/year=*/chunks.jsonl` (71 files) | dataset-clean | labeled chunks 2.34M | E3/E4 | present | ~2.7 GB |
| `corpus/ecourts/metadata/year=*/metadata.parquet` (71 files) | dataset-meta | per-doc metadata 39,073 rows | E3/E4 | present | date range 1950-03-14–2020-12-18 |
| `corpus/dedup_matches.csv`, `dedup_report.md`, `temporal_overlap_audit.md`, `dataset_manifest.md` | corpus-governance | alignment/dedup/temporal audit | E3/E4 | implemented | rejections/ambiguities CSVs referenced but absent locally (gitignored) |
| `retrieval/bm25.sqlite` | index | FTS5 BM25 + temporal side table | E3/E4 | present (2.27 GB) | 2,036,981 rows each table |
| `answer_key/authority_answer_key.json` (33 entries) + `dev_retrieval_probe.json` (9) + manifest | answer key | source-verified expected authorities | E3/E4/RQ2 | implemented, frozen (30 eval) | target 40; 75/100 do NOT exist |
| `artifacts/*.json/*.md` (~120 files) | generated artifacts | frozen results, audits, drafts | all | present | E1/E2/E3/E4 + weeks 4–16 |
| `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/` | checkpoint | canonical E2 weights | E2/E3/E4 | present | model.safetensors 438 MB |
| `artifacts/e2_hf_cache/` | model cache | InLegalBERT base | E2 | present (hub blobs) | 2×534 MB blobs |
| `demo/index.html app.mjs data.mjs style.css verify.mjs verify-browser.mjs README.md` | demo | static precomputed UI (7 cases) | demo/RQ3 | implemented | no live retrieval |
| `submission/paper.md paper.html paper.pdf MANIFEST.md figures/` | documentation/paper | frozen paper + figures | all | implemented | paper §§ cited in §4 |
| `PROJECT_CHECKLIST.md`, `README.md`, `TRANSFER_README.md`, `TRANSFER_MANIFEST.json` | documentation | scope/checklist/transfer guard | all | implemented | Wk1–16 checked except Wk11 outreach blank |
| `requirements.txt`, `pytest.ini`, `.gitignore`, `.gitattributes` | env/config | minimal pins, test paths, ignores | repro | implemented | torch/transformers only via docker/host |

Unusually large files/dirs: `retrieval/bm25.sqlite` (2.27 GB); HF blobs 2×~534 MB; `checkpoint-6318/model.safetensors` (~438 MB); per-year `chunks.jsonl` up to ~95 MB (2019); `single_train.parquet` (~56 MB). `corpus/ecourts/pdfs/` dominates total size (~21 GB, 39,070 PDFs).

Git state (verified `git status`): `No commits yet on main...origin/main [gone]`, all files untracked — transfer/clone copy; full history absent in this copy. Not a code defect per se but noted for provenance.

---

## 3. Actual Architecture

Real data flow (from code, not README alone):

`user query (facts text)` → `facts.py:extract_case_facts()` [E1/E2 input; E3/E4 query = frozen facts] → `retrieval.py:fts_query(salient_tfidf)` (≤32 terms) → `evidence_pipeline.py:temporal_preranked_bm25_sql()` (`decision_year < query_year` inside SQLite before `ORDER BY bm25 LIMIT 100`) → Postgres `corpus_chunks` provenance join + `retrieval.py:exclude_query_duplicate()` (crosswalk `corpus/dedup_matches.csv` + ≥100 shared 6-grams AND ≥80% source coverage via `alignment.py`) + `temporal.py:assess_temporal_eligibility()` recheck → `select_diverse_evidence(k100→≤5, 1/source, eligible-only, BM25 desc)` → branch A (prediction): `evidence_augmented_prediction.py:EvidenceAugmentedPredictor.predict(facts+\n\n+passages)` (frozen E2 ckpt-6318, CUDA) → label; branch B (explanation): `grounded_answer.py:render_grounded_answer()` (5-section extract-only) → `citation_verifier.py:verify_answer_citations()` + `evaluate_against_answer_key()` → `demo/*.mjs + serve_week16_demo.py` (7 frozen cases, parity-checked).

Architecture table (COMPONENT | FILE | IMPLEMENTATION | INPUT | OUTPUT | STATUS):

| COMPONENT | FILE | IMPLEMENTATION | INPUT | OUTPUT | STATUS |
|---|---|---|---|---|---|
| Preprocessing / legal NLP (facts gate) | `src/legal_xai/facts.py` (`extract_case_facts`, `facts_input_is_eligible`) | regex earliest closing/dispositive cue, else 60% cap, sentence-align ≥240ch; eligible iff retained≥10% AND ≥100 words | ILDC text + `config/facts_extraction.json` (`ildc-predecision-facts-v1`) | `FactsExtractionResult` | implemented, runnable (stdlib-only) |
| Corpus clean/chunk | `src/legal_xai/corpus.py` | edge-line furniture stoplist, margin/noise strip, 220-word/4-sent chunks, non-evidentiary filter | raw PDF pages | `TextChunk`s | implemented, runnable |
| Identity gate | `src/legal_xai/alignment.py` | title/party ≥2 shared + ≥0.8 coverage AND ≥100 shared 6-grams | ILDC text, source text/title | `ContentAlignment` | implemented, runnable |
| Query construction | `src/legal_xai/retrieval.py` (`salient_query_terms`, `fts_query`) | TF-IDF segments + procedural stopwords + statutory boost, ≤32 terms; legacy-first-32 retained | facts text | FTS5 OR string | implemented, runnable (needs sklearn 1.9.0) |
| Temporal eligibility | `src/legal_xai/temporal.py` (`assess_temporal_eligibility`, `partition_evidence_candidates`) | year compare: `<` eligible, `==` ambiguous_excluded, `>` ineligible, unparseable excluded | query year, precedent date | `TemporalDecision` | implemented, runnable |
| Retrieval + evidence selection | `src/legal_xai/evidence_pipeline.py` (`retrieve_temporal_candidates`, `select_diverse_evidence`, `temporal_preranked_bm25_sql`) | FTS5 MATCH + `decision_year<?` pre-rank, Postgres provenance, per-source dedup, persist run | query id/year/text, k=100, `retrieval/bm25.sqlite`, DB URL, dedup CSV | `CandidateRetrieval` → ≤5 diverse | implemented; runnable only with DB + index + corpus + dedup |
| Explanation renderer | `src/legal_xai/grounded_answer.py` (`render_grounded_answer`, `assert_answer_grounded`) | extract-only copy of verbatim text + 7 provenance fields; frozen order/version; sufficiency 0/1/≥2 | eligible candidates | `GroundedAnswer` dict | implemented, runnable (pure) |
| Citation/provenance verifier | `src/legal_xai/citation_verifier.py` (`verify_answer_citations`, `evaluate_against_answer_key`) | 5-check contract + parallel-citation reconciliation + run-membership/duplicate/temporal | answer, corpus records, run chunk IDs, answer key | pass/fail + answer-key measure | implemented, runnable (pure) |
| Answer-key gate | `src/legal_xai/answer_key.py` | ILDC fixed-test-only population gate | parquet IDs, cleaning record | split membership | implemented (needs parquet) |
| Outcome predictor (E3/E4) | `src/legal_xai/evidence_augmented_prediction.py` (`EvidenceAugmentedPredictor`) | facts+\n\n+passages → 512/overlap-50 full-coverage windows → CUDA fp16 → mean-logit argmax; checkpoint-SHA-gated | facts + evidence texts + `config/e3_e4_*.json` | `OutcomePrediction` | implemented; runnable only with CUDA + ckpt-6318 + HF base |
| Demo | `demo/*` + `scripts/serve_week16_demo.py` | static precomputed UI, allowlisted stdlib server | frozen artifacts | displayed briefs | implemented, runnable (no live retrieval) |

---

## 4. Research Scope

Extracted verbatim from spec sources (no rewriting):

- Objective (`README.md:1-3`; `submission/paper.md:11`): auditable legal research over historical Supreme Court judgments; E1/E2 facts-only baselines; E3/E4 retrieve+verify evidence and emit predictions by reusing frozen E2 checkpoint with inference-time augmentation. Research aid, not advice.
- Problem (`submission/paper.md:8-9,19-20,23-27`): plausible prose can cite nonexistent/misattributed/post-dated/never-retrieved authorities (cites *Pooja Ramesh Singh v. J&K Bank*, 2026 INSC 668). Formalized as query `(q, Yq, Fq)` with strict earlier-year admission; three evidence questions (Recovery @100, Integrity of displayed citations, Presentation) + prediction as fourth contextual task.
- Gap (`submission/paper.md:31-33`): combined auditability when linking historical case to external corpus (identity validation, time-restricted candidates, passage–provenance tie, visible retrieval failure); bounded novelty (alignment gating, year pre-rank, exact/run verification, recovery-vs-validity separation); explicitly not first RAG/model/benchmark.
- RQs (final, `submission/paper.md:57-60`): RQ1 E1-vs-corrected-E2 on fixed 1,503 test; RQ2 recovery @5/@100 + citation checks under final config; RQ3 structured-vs-unstructured with evidence held constant; RQ4 E3/E4 evidence-augmented accuracy/macro-F1 on 30-case subset. Note: earlier E3/E4-outcome-comparison plan retired (`artifacts/paper_draft.md:69`), superseded by current RQ4.
- Hypotheses (`submission/paper.md:64-66`): H1 (E2> E1 via domain pretraining) NOT supported on frozen 1,503; H2 (pre-rank improves recovery) supported in bounded 30-case comparison; H3 (structured preferred) directionally consistent in 7-case self-review but non-independent, no general claim.
- Objectives (executed): dual-corpus workflow (5,391 syntactic → 11 aligned); three bounded retrieval corrections (salient full-input terms, coverage-qualified self-match guard, pre-rank temporal); recovery-vs-integrity separation; E1/E2 + E3/E4-30 + format observation.
- Scope: ILDC 7,593 (5,082/994/1,517 → 1,503 eligible) for E1/E2; eCourts 1950–2020 39,069 PDFs → 2,343,435 labeled / 2,036,981 unique chunks for E3/E4; answer key 30 fixed-test; explanation review 7 pairs.
- Exclusions: no adjudication/advice; no per-authority legal-correctness claim; English SCI only; same-year/missing-date excluded; 3 one-page PDFs + 14 test records + 2019_890 excluded; no accounts/multi-user/live-retrieval/production DB; 138 nonmatching citations unlabeled (not "irrelevant"); FEER/FCER removed; no canonical E4−E3 delta.
- E1/E2/E3/E4: per configs — E1 TF-IDF(1-2,100k,sublinear)+LogReg C∈{0.1,1,10}→C=10, seed 202605; E2 InLegalBERT `b5ecfed8`, corrected 512/50 mean-logit primary + majority-vote secondary, 3ep, seed 202607 (256-prefix discarded); E3 `week11-bm25-salient-terms-preranked-temporal-v3` k100→top5 1/source; E4 verifier-v2 + renderer-v1 extract-only frozen order; E3/E4 share predictor, identical 0.6667/0.6032 on n=30.
- Temporal protocol: eligible iff `precedent_year < query_year`; same-year ambiguous_excluded; missing excluded; applied BEFORE BM25 ORDER/LIMIT. Day-level unavailable in ILDC public release (dataset constraint).
- Explainability: every material statement = exact passage + provenance; frozen non-inferential conclusion; insufficiency stated; fixed order issue→authorities→evidence→conclusion→uncertainty; RQ3 rates clarity/traceability/trust/limits (7/7 structured, self-review).
- Citation/provenance: persisted chunk/source IDs, citation, exact date, court, PDF/page/char locators; run records query/year/text/index-version/policy/rank/score/status; 5 hard checks; matching after verification; duplicate rule ≥100 6-grams + 80% coverage.
- Metrics (frozen denominators kept separate: 1,503 / 30+150 / 7): §9–12 values.
- Governance: human reviewer responsible; fail-closed exclusions; transparent negatives; future deployment needs controls/licensing/privacy/independent eval/monitoring.
- Reproducibility: freeze-v4 + replay contracts + hashes/seeds (details §20).
- Limitations (9, `submission/paper.md:289-325`): English/source; extraction no-gold; n=30 era-skewed; single-authority reference, 138 unlabeled; half absent @100; year granularity; bundled verification; self-review + uncalibrated uncertainty; semester prototype.
- Future: 75–100 era-balanced key + McNemar; blinded raters + Fleiss κ; hybrid dense-sparse with controls retained (revision-stage, not current claims).
- Scope-freeze: no post-test tuning; frozen IDs; no further retrieval/query change; populations final (10-case extension = separate round); read-only synthesis; transfer guard (don't overwrite frozen 30/artifacts); consistency gate (12 checks, populations separate, no stale 0.0815/135/superseded as final).

REQUIREMENT → IMPLEMENTATION → EVIDENCE → STATUS → GAP table (condensed; full evidence in §§5–22):

| Requirement | Implementation | Evidence | Status | Gap |
|---|---|---|---|---|
| RQ1 E1 vs E2 (n=1503) | both trained, frozen, compared | `artifacts/e1_baseline_results.json`, `e2_chunk_pool_results.json`, `e1_e2_comparison.json` | COMPLETE | none blocking; CIs unreported |
| RQ2 recovery + integrity (n=30/150) | final pre-rank config evaluated | `artifacts/week11_temporal_prerank_evaluation.json`, `e3_e4_*.json` | COMPLETE (bounded) | n=30 small; 15/30 absent; single-authority ref |
| RQ3 format with evidence constant | 7-pair packet + self-review | `artifacts/week13_*` | PARTIAL (infrastructure + self-review only) | independent raters, κ, significance missing |
| RQ4 E3/E4 prediction (n=30) | shared predictor, parity-enforced | `artifacts/e3_e4_evidence_augmented_evaluation.json` | COMPLETE (bounded) | n=30 small; no delta metric by design |
| Temporal P1 (year order) | pre-rank + recheck + verifier | `src/legal_xai/temporal.py`, `evidence_pipeline.py:34-40`, 3000/3000 + 150/150 eligible, 0 viol | COMPLETE (P1) | P2 exact-date impossible (data constraint) |
| Citation/provenance 5-checks | verifier-v2 + run persistence | 150/150 grounded/provenance-valid | COMPLETE (bounded) | bundled causal attribution absent by design |
| 40-case key | 30 eval + 3 dev done | `answer_key/*.json`, freeze | PARTIAL | 10 cases pending human work |
| Repro freeze + replay | freeze-v4 + 2 replay scripts | week10/week16 audits PASS | COMPLETE (local-asset model) | external-asset + DB-up prerequisites remain |

---

## 5. Dataset Audit

ILDC (`corpus/ildc/`, verified sizes; row counts from subagent parquet-metadata read, consistent with `corpus/dataset_manifest.md` + `config/datasets.json`):

| File | Bytes | Rows | Columns | Text | Labels | Metadata/dates/citations | Status |
|---|---|---|---|---|---|---|---|
| `single_train.parquet` | 56,421,032 | 5,082 | 33 physical (`id,text,label` + nested expert_1..5) | yes (e.g. 18–31k chars sampled) | yes (0:3147, 1:1935 sampled) | `id` year-prefix 1947–2019; no SHA recorded in repo (gitignored) | present, appears complete |
| `single_validation.parquet` | 10,770,658 | 994 | 8 (`id,text,label,expert_1..5`) | yes | yes | same `id` scheme | present |
| `single_test.parquet` | 16,839,899 | 1,517 | 33 physical | yes | yes | `id` min 1950_14 max 2017_61 sampled | present |
| Total | — | 7,593 | — | — | — | revision `d16219ad` per `config/datasets.json`; per-split SHA in freeze (not per-file hash in manifest) | matches manifest |

Eligible evaluation population after shared facts-sufficiency rule: train 5,020 (excl 62), val 983 (excl 11), test 1,503 (excl 14); eligible-ID SHAs + source SHAs recorded in `artifacts/e1_baseline_results.json:104-233`.

Missing-dataset report: no missing ILDC splits. `datasets/`, `corpus/index`, `DB/`, `index/`, `*.db` paths do NOT exist (verified `Test-Path False`) — expected locations are `corpus/` + `retrieval/bm25.sqlite` + Postgres via compose. Referenced-but-absent locally (gitignored): `dedup_alignment_rejections.csv`, `temporal_ambiguities.csv` (cited in manifest/report; aggregates present in `dedup_report.md`/`temporal_overlap_audit.md`).

---

## 6. Corpus Audit

Actual location: `corpus/ecourts/` (`acquisition_record.json`, `cleaning_record.json`, `cleaned/year=1950..2020/`, `metadata/year=1950..2020/`, `pdfs/year=1950..2020/`).

- Files/records: 71 cleaned `chunks.jsonl` (total 2,712,095,037 B; line-count total **2,343,435** = manifest's labeled chunks); 71 `metadata.parquet` (43,618,896 B; **39,073 rows**); 39,069 PDFs (~21 GB). `provenance_load.json`: 2,343,435 read → 2,036,981 unique loaded → 306,454 duplicate chunk_ids skipped. BM25 holds 2,036,981 (matches).
- Date range: metadata parsed 1950-03-14 to 2020-12-18, 0 unparseable; chunks carry `decision_date` DD-MM-YYYY + `year`.
- Metadata fields: chunks: `case_id,citation,title,petitioner,respondent,decision_date,court,disposal_nature,year,path,source_id,chunk_id,pdf_file,...`; metadata parquet: 18 cols incl. judges, CNR, languages, raw_html, scraped_at.
- Source: eCourts-mirror PDFs (answer-key URLs scraped from `scr.sci.gov.in` per key entries; corpus acquisition record scope 1950–2020 English, `updated 2026-08-27`).
- Cleaned/chunk availability: yes (71/71 years). Dedup: `dedup_matches.csv` (1,304 rows, all passed alignment-gated) + `dedup_report.md` (7,593 ILDC × 39,073 eCourts → 33,892 distinct IDs → 5,391 syntactic → 2,474 title/party → 1,304 accepted / 7,623 rejected). Provenance: per-chunk locators persisted; runs persist query/policy/rank/score. Hashes/manifests: aggregate `f0229bbb...` in freeze (local-bytes identity); per-file hashes not recorded; acquisition/cleaning records carry no hashes.
- Anomaly noted: `cleaning_record.json` years[] sums to only 15 docs / 2,037 chunks (repair/QA overlay, v2-quality-gated-ocr, 14 repair IDs) — NOT the full 2.3M rebuild; full totals from `provenance_load.json` + `dataset_manifest.md`.
- Missing: nothing blocking current frozen claims; per-file corpus hashes and the two gitignored diagnostic CSVs are absent locally (UNKNOWN whether retained elsewhere).

---

## 7. Index and Database Audit

- BM25 index EXISTS: `retrieval/bm25.sqlite`, 2,269,376,512 B, mtime 2026-09-11. Only file in `retrieval/`. Schema (from read-only `sqlite_master` inspection): `chunks_fts` FTS5 (`chunk_id UNINDEXED, chunk_text, unicode61 remove_diacritics 2`) + side tables + `chunk_temporal_metadata(chunk_id PK, decision_year NOT NULL)` + year index. Counts: 2,036,981 rows each; year min 1950 max 2020. Metadata: `artifacts/bm25_index.json` (`fts5-bm25-unicode61-temporal-v2`, 2,036,981 chunks, bytes recorded). Version: index version string recorded; SQLite engine version UNKNOWN (not recorded; not queried beyond read-only counts in this audit).
- FTS5 tables: present (above). Provenance DB schema: defined in `scripts/load_provenance.py` (`corpus_chunks`, `retrieval_runs`, `retrieval_results`); live-DB schema NOT inspected here (service down).
- PostgreSQL/docker config: `compose.yaml` single service `postgres:16-alpine`, `legal-xai-postgres`, `127.0.0.1:54329:5432`, volume `legal_xai_postgres_data`, password via env guard. Dump/backup: none found (no `.dump`/`.sql`/backup files). Retrieval-run persistence: implemented in code (`retrieval_runs`/`retrieval_results`) + frozen JSON artifacts; live rows unverifiable here.
- DB connectivity (this audit machine): **service not running / port unavailable / Docker daemon unavailable** — `psycopg` connect to 127.0.0.1:54329 failed (connection refused/timeout path), `docker ps` failed (daemon pipe missing). Credentials NOT the blocker (default local URL present, env-overridable; freeze explicitly does not freeze credentials). Distinction: **schema present in code + dump missing + DB unavailable due to service-down, NOT asset-deleted**; `bm25.sqlite` + JSON artifacts allow offline verification of frozen claims without live DB.

---

## 8. Model and Environment Audit

E1: TF-IDF(1–2g, min_df 2, max 100k, sublinear, L2) + LogReg liblinear C∈{0.1,1,10} → selected C=10 on validation, refit train+val once (`config/e1_baseline.json`, seed 202605). Training script `scripts/train_e1_baseline.py`. Saved model `artifacts/e1_reconstructed_model.joblib` (2,079,388 B, SHA `60f407...` per freeze). Results §9.

E2: base `law-ai/InLegalBERT` rev `b5ecfed8ed6cf9d25a3cb8225a8c52f161f7401a` (`config/model.json`, `e2_chunk_pool.json`). Checkpoint **checkpoint-6318** present: `config.json` (760 B), `model.safetensors` (437,958,648 B, SHA `924a5bb9...` per freeze/TRANSFER_MANIFEST), `trainer_state.json`, `training_args.bin`. Tokenizer files: only via `artifacts/e2_hf_cache/hub/models--law-ai--InLegalBERT/` blobs (2×~534 MB + small files); `artifacts/e2_model/` ABSENT (expected — cache layout used). Training config: 512 length, 50 overlap, mean-logit primary / majority-vote secondary, 3 epochs, lr 2e-5, wd 0.01, warmup 0.1, batch 2×8, fp16, adamw_torch, seed 202607. Scripts: `train_e2_chunk_pool_cached.py`, `prepare_e2_chunk_pool_cache.py`, `infer_e2_checkpoint_predictions.py` (exact-reproduction gate).

E3/E4: same frozen ckpt-6318, inference-only, evidence-augmented input, 512/50, mean-logit argmax, threshold null, CUDA fp16-autocast, batch 2 (`config/e3_e4_evidence_augmented_prediction.json`). No distribution shift by design (identical checkpoint/config/pooling); only input distribution changes (facts-only → facts+passages), which is the studied augmentation. No separate E3/E4 checkpoints.

Runtime (verified): Python **3.13.14** on audit host (freeze records 3.11.9 — host differs, noted); `scikit-learn 1.9.1` (freeze 1.9.0), `pyarrow 25.0.1` (freeze 21.0.0), `psycopg 3.3.5` (freeze 3.3.4), `pytest 9.1.1` (matches); **`torch` NOT installed, `transformers` NOT installed** on host (verified `pip show` miss) — hence 2 test collection errors; CUDA/GPU availability UNKNOWN on host (not probed; E3/E4 inference requires CUDA per config); Postgres server version recorded 16.15 in freeze, service down here; Java/Node not required except demo `verify-browser.mjs` (Playwright/Edge, not run here). Package locks: no `*.lock` for Python (6 `.lock` files are HF hub locks); versions pinned in `requirements.txt` (4 pkgs) + `docker/e2.Dockerfile` (torch image + transformers 4.46.3 for training vs 5.15.0 host replay, roles separated in freeze).

---

## 9. E1 Audit

Intent: frozen Week-5 facts-only sparse baseline on shared pre-decision inputs. Impl: `scripts/train_e1_baseline.py:62-71,192-200`. Config: `config/e1_baseline.json` (above). Population: source 5,082/994/1,517 → eligible 5,020/983/1,503 (excl 62/11/14); labels train 0:3116/1:1904; test 0:749/1:754. Splits: fixed ILDC files; selection on validation only. Metrics (N=1503 test): acc **0.61344**, macro-F1 **0.612342**, C0-F1 0.632975, C1-F1 0.591708, CM [[501,248],[333,421]]; val acc 0.613428 (C=10); majority-1 baseline 0.501663 (+11.18pp). Results: `artifacts/e1_baseline_results.json/.md`, `e1_test_predictions.json`, `e1_reconstructed_model.joblib`, `e1_e2_comparison.json`, `e1_exclusion_audit.json/.md`. Frozen: yes (freeze SHAs). Reproducible: yes (`week16` E1 pass, records_exact, raw SHA `9af1cad...`). Verdict: **real executed result** (not fixture/synthetic).

Metric table: E1-acc 0.61344 (N=1503, test, `e1_baseline_results.json`, REAL); E1-macroF1 0.612342 (same, REAL).

---

## 10. E2 Audit

Intent: corrected facts-only InLegalBERT chunk-and-pool fixing 256-prefix truncation. Impl: `train_e2_chunk_pool_cached.py`, `prepare_e2_chunk_pool_cache.py`, `infer_e2_checkpoint_predictions.py`. Config: `config/e2_chunk_pool.json` (512/50, mean-logit primary, seed 202607). Discarded predecessor: `train_e2_baseline.py` + `config/e2_baseline.json` (256-token, ckpt-939, test acc 0.5695/F1 0.5575, 99.20% truncated) — retained for traceability, NOT the final E2. Population: same eligible IDs/SHAs as E1; windows train 33,702 / val 6,054 / test 9,576; fully-covered 1.0; median 5, max 68. Metrics (N=1503): mean-logit acc **0.596806** / F1 **0.592358** (CM [[527,222],[384,370]]); majority-vote acc 0.601464 / F1 0.593682; best ckpt-6318 (val 0.612411). Results: `e2_chunk_pool_results.json/.md`, `e2_test_predictions.json`, `e2_chunk_pool_training_audit.json`, `e2_correction_manifest.json`, ckpt-6318 files. Frozen: yes. Reproducible: yes (`week16` E2 pass, 9,576 windows, raw SHA `43f33a...`; training env torch 2.5.1+cu124/RTX3050/transformers 4.46.3, replay host 5.15.0 per freeze roles). Verdict: **real executed result**; discarded-256 = real-but-superseded (must not be cited as final).

---

## 11. E3 Audit

Intent: temporally constrained retrieval + diverse selection + (later revision) evidence-augmented prediction with frozen E2 checkpoint (no retraining). Impl files: `src/legal_xai/{retrieval,evidence_pipeline,grounded_answer(decoder side),evidence_augmented_prediction}.py`, `scripts/run_evidence_pipeline.py`, `run_e3_e4_evidence_augmented_evaluation.py`. Config: `config/evidence_selection.json` (`week11-bm25-salient-terms-preranked-temporal-v3`, k100→5, 1/source) + `config/e3_e4_evidence_augmented_prediction.json`. Population: 30-case answer-key subset of ILDC fixed test. Eval: §13 metrics. Results: `artifacts/e3_e4_evidence_augmented_evaluation.json` (E3 section), `e3_e4_prediction_error_analysis.json/.md`. Frozen: yes. Reproducible: yes (bounded, CUDA; week16 pass after `retrieved_not_selected`→`selected_measure` fix). Verdict: **real executed result** (N=30, small). E3 vs E4 prediction identical by parity enforcement (`run_*.py:135-136` raises on mismatch).

---

## 12. E4 Audit

Intent: E3 evidence + extract-only verified explanation + 5-check citation verification, then same shared predictor. Impl: E3 stack + `src/legal_xai/citation_verifier.py` (verifier-v2), `grounded_answer.py` (renderer-v1), `scripts/run_grounded_answer_pipeline.py` (+ in-file `verify_rendered_explanation`), `verify_citations.py`. Config: `config/citation_verification.json` + `grounded_answer.json`. Population/metrics: same N=30/150 as E3; E4 prediction acc **0.666667** / F1 **0.603175**, CM [[4,3],[7,16]]; integrity 150/150 grounded/provenance/eligible, 0 violations/unsupported; `E3correct_E4wrong 0/30`. Results: same `e3_e4_*` files (E4 sections) + `week9_real_e3_*` demo + `week10_*replay*`. Frozen/reproducible/real: yes (same freeze/replay as E3). Note: E4 is NOT a single-variable ablation of E3 (joint verification bundle, `submission/paper.md:182`); no canonical E4−E3 delta by design. Week-11 outcome fields were `available:false`; outcome added 2026-09-06 without overwriting evidence artifacts.

---

## 13. Retrieval Audit

Pipeline: `retrieval.py:salient_query_terms` (TF-IDF segments, ≤32, statutory boost) → `fts_query(salient_tfidf)` → `evidence_pipeline.py:temporal_preranked_bm25_sql` (MATCH + `decision_year<?` before ORDER/LIMIT) → Postgres provenance + `exclude_query_duplicate` (dedup CSV + 100-phrase/80% rule via `alignment.py`) → `select_diverse_evidence` (eligible-only, 1/source, BM25 desc) → persist run. Top-k: candidate 100, display 5. Scores: BM25 retained per candidate; selection by (−BM25, rank).

Metric existence/values (final pre-rank config, N=30/150, `week11_temporal_prerank_evaluation.json` + `e3_e4_*.json`): Recall@5 **0.40 (12/30)** EXISTS; Recall@100 **0.50 (15/30 = 12 selected + 3 retrieved-not-selected)** EXISTS; authority precision **0.08 (12/150)** EXISTS; authority recall **0.40** EXISTS; authority F1 **0.133333** EXISTS (ceiling 30/150=0.20; observed 40% of ceiling); citation groundedness **1.0 (150/150)** EXISTS; provenance validity **1.0 (150/150)** EXISTS; temporal violation rate **0.0 (0/150)** EXISTS; unsupported claim rate **0.0** EXISTS. Buckets: selected 12 (IDs §-subagent), retrieved-not-selected 3 (1980_133 r15, 1981_55 r28, 1985_40 r78), absent 15. Superseded post-rank baseline (for contrast only): R@5 0.1667, R@100 0.40, 135 items (4.5/case) vs final 150 (5.0/case).

Answer-key structure: **one expected authority per case** (no multiple-authority evaluation); relevance labels = expected-authority identity (not graded relevance); temporal labels = `eligible_by_year` per entry + query/authority dates. 138/150 nonmatching displayed citations are unlabeled (must not be called irrelevant).

---

## 14. Temporal Integrity Audit

Implementation: `temporal.py:assess_temporal_eligibility` (`<` eligible; `==` ambiguous_excluded; `>` ineligible; unparseable → excluded_missing_metadata) + `partition_evidence_candidates`; SQL predicate `decision_year < ?` before ORDER/LIMIT (`evidence_pipeline.py:34-40`); Python recheck on candidates; renderer emits only eligible; verifier re-checks temporal (`citation_verifier.py`). Year-level policy: strictly earlier year. Exact-date policy: exact eCourts dates parsed/stored, but **decision rule uses year granularity** (ILDC query side is year-granular). Same-year: excluded (ambiguous) but retained for audit. Missing: excluded. Duplicates: excluded via alignment-gated rule. Evidence: final eval 3,000/3,000 candidates eligible + 150/150 displayed eligible; post-rank baseline had 1,712 later + 267 same-year among 2,743 (motivating pre-rank). Tests: `test_temporal.py` 8 tests (P1/P2/later/missing/partition).

P1/P2 verdict: **P1 (year-granular ordering) SUPPORTED**; **P2 (exact-date ordering) NOT supported** — implementation is intentionally year-granular; paper states day-level query dates unavailable in ILDC public release (dataset constraint, `submission/paper.md:312`). Do not claim exact temporal ordering.

---

## 15. Citation and Provenance Audit

End-to-end trace (case `2008_1629`, from frozen artifacts): final citation `[2006] SUPP.2 S.C.R.582` (E1 slot) → authority identity `U. Raghavendra Acharya`, source `S_2006_2_582_600`, date 2006-05-12 (answer key expects `(2006) 9 SCC 630` — parallel reporter reconciled via stable source ID) → source document chunk `S_2006_2_582_600::p0015::c004`, PDF p15 chars 1275–2007 → retrieval run rank 1, BM25 ~59.12, temporal eligible → provenance validation (7 fields exact) → final output (E4 explanation E1 slot verbatim + metadata exact, frozen non-inferential conclusion) → verifier `passed:true, failures:[]`.

Verification rules (`citation_verifier.py:113-174`): authority-without-linked-evidence; corpus-chunk-missing; corpus-metadata-mismatch; passage-mismatch; authority-metadata-mismatch; query-duplicate-source; temporal ineligible/ambiguous/missing; not-retrieved-for-query; unsupported-authority-field. Answer-key matching only after checks pass; parallel SCC↔SCR reconciled via source ID → citation → title+date. Timing: **both** — pre-render gating (eligible-only selection) AND post-render verification (`assert_answer_grounded` + `verify_answer_citations`). Provenance validity ≠ legal correctness (138 nonmatches unlabeled; paper explicitly limits claim).

---

## 16. Answer-Key Audit

`authority_answer_key.json`: schema `week7-authority-key-v3`, target 40, complete 30; **entries 33 = 30 `evaluation` + 3 `dev_example` (2019_890×3)**; all `temporal_status eligible_by_year`; query years 1971–2019, authority dates 1956–2009. `dev_retrieval_probe.json`: 9 entries (1980s:5, 1990s:4). Schema (`config/authority_answer_key_schema.json`): source-first, `independent_of_system_retrieval`, prohibited source = project retrieval output; allowed statuses evaluation/dev_example. Source verification: eCourts-mirror PDFs, `scr.sci.gov.in` URLs, `verified_on 2026-08-29/30`, native-text. Dates/relevance/temporal: per-entry query/authority dates + relationship + eligible flag; single authority per case (no graded relevance). Duplicates: gated via 1,304-pair crosswalk. Unresolved: 10-case backlog to reach 40 (must be separate round); alignment audit 20 pass / 9 replaced + 2013_35 crosswalk-fixed, still 30; sanity check 30/30 pass; era skew 1980s 13/30.

Count verdict: **30 cases** (evaluation). NOT 75, NOT 100. (`100` = candidate-k depth; `1503` = full test N; `30/40 = 75%` of target — the only sense in which "75" appears.)

---

## 17. Explainability Audit

Implemented: structured explanation with fixed order (issue, authority, evidence, conclusion, uncertainty/limitations); verbatim passages + 7-field citation cards + source traceability (PDF/page/char locators + run IDs); frozen non-inferential conclusion + insufficiency signaling + uncertainty boilerplate. Attribution/model explanations (feature importance, etc.): NOT implemented (out of scope; extract-only design). Tests: `test_grounded_answer.py` 8 tests (extract-only, order, rejection of altered/ineligible/unsupported). Machine QA: Week-8 5 synthetic grounding passed; Week-10 E4 5/5; Week-11/12 spot 0/5 highlights-not-evidence.

---

## 18. Human Evaluation Audit

Status: **infrastructure + self-review only; independent review ABSENT**. Packet exists (`artifacts/week13_review_packet.md`, 7 fixed pairs: 2008_1629, 1980_105, 1980_133, 1981_55, 1985_40, 1997_792, 2013_35; citation parity 7/7 + 35/35; A/B structured-vs-unstructured with evidence held constant; questions clarity/traceability/trust/limits; means structured 4.57/4.57/4.43/4.43 vs unstructured 2.71/2.29/2.86/3.00; 7–0–0 preference, narrow for 1980_133/2013_35; boilerplate uncertainty miscalibrated on 2013_35). Responses: 1 reviewer (author), `completed 2026-09-03`, `outside_reviewer:false`, `author_self_review_fallback`. Reviewers: 0 independent. Agreement stats: none (Fleiss κ listed as future work). An empty packet was never counted — but the completed packet must NOT be reported as independent evidence (`week13_review_status.md`, `week14_results_evidence_inventory.md` guard). RQ3 therefore remains pending independent human data.

---

## 19. Test Audit

Files: 11 test files. Tests (verified by read-only run on host Python 3.13): full suite **2 collection errors** (`test_e2_chunk_pool_windows.py`: `transformers` missing; `test_evidence_augmented_prediction.py`: `torch` missing) → run excluding those 2 files: **75 passed, 0 failed/skipped**. Per-file: `test_citation_verifier` 18, `test_retrieval` 14, `test_grounded_answer` 8, `test_temporal` 8, `test_facts`/`test_corpus`/`test_alignment`/`test_answer_key`/`test_evidence_pipeline` 4–8 each (exact per-file counts for the 9 runnable files: 75 total; combined rerun of temporal+retrieval+verifier alone = 40 passed). Integration tests: evidence-pipeline/grounded-answer/augmented-prediction exercise cross-module contracts with fixtures (no live DB/GPU/LLM calls in bodies). Environment-dependent: the 2 error files require `torch`/`transformers` (E2 image provides; host lacks) — WHY needed: window-contract + predictor unit tests import those libs; IMPACT: E2-predictor contracts unverifiable on bare host, verifiable in E2 image. GPU-dependent: none in tests (predictor CUDA path is runtime config, not test). Collection errors: 2 (above). No destructive commands executed.

| TEST | ERROR | DEPENDENCY | WHY NEEDED | IMPACT |
|---|---|---|---|---|
| `test_e2_chunk_pool_windows.py` | `ModuleNotFoundError: transformers` | `transformers` (4.46.3 in E2 image) | imports `prepare_e2_chunk_pool_cache` window fn | window-contract tests unrunnable on host; runnable in E2 image |
| `test_evidence_augmented_prediction.py` | `ModuleNotFoundError: torch` | `torch` (CUDA image) | imports predictor module | predictor unit tests unrunnable on host; runnable in E2/CUDA image |

---

## 20. Reproducibility Audit

Freeze: `config/reproducibility_freeze.json` (`final-reproducibility-freeze-v4-e3e4-prediction`) + `artifacts/week10_reproducibility_freeze.md`. Metadata tracked: ILDC splits (rows + SHA + bytes), facts config hash, eCourts aggregate (71 files / 2,343,435 records / `f0229b...`), BM25 SHA (`3187f7...`, gitignored 2.27 GB), dedup/cleaning records, E1 joblib SHA (`60f407...`), ckpt-6318 SHAs (`924a5bb9...`), configs, splits, answer key, retrieval version, week10 regression + dev recheck + temporal evaluation SHAs. Seeds: E1 202605; E2/E3/E4 202607. Configs: frozen IDs (§4). Dependency versions: recorded in freeze (python 3.11.9, torch 2.13.0+cu130, transformers roles 4.46.3-train vs 5.15.0-replay, postgres 16.15, sklearn/pyarrow/psycopg/pytest); mutable upstream tags documented as limitation. Dataset versions: ILDC `d16219ad` + per-split SHA; index/model hashes: yes; code version: build-definition commit `d801147...` recorded BUT full git history absent in this transfer copy (no commits). Docker: `compose.yaml` (postgres:16-alpine) + `docker/e2.Dockerfile` + `Dockerfile.ocr` recorded with digests where available. Manifest: `TRANSFER_MANIFEST.json` + `submission/MANIFEST.md`. Restore: replay contracts (`run_week10_reproducibility_replay.py`: two E4 runs match excl. UUIDs; `replay_e3_e4_evidence_augmented_evaluation.py`: fresh E3/E4-only run matches excl. run IDs) — verified `week16` 14/14 doc checks + 34/34 hashes + clean-clone replay #2 PASS (replay #1 FAIL documented + fixed: `retrieved_not_selected`→`selected_measure` bookkeeping). DB backup: none. External assets required: ILDC parquets (gitignored, present here), eCourts PDFs/cleaned (gitignored, present here), `bm25.sqlite` (gitignored, present here), ckpt-6318 (gitignored, present here), HF base (cache present here), Postgres service (down here), CUDA (per config; host status UNKNOWN).

Reproducible from repo alone: **code + configs + frozen JSON claims + tests (minus torch files) — yes; full empirical rerun — no** (requires large gitignored assets + Postgres + CUDA + E2 image). Do not claim full standalone reproducibility.

---

## 21. Security and Governance Audit

Checks: secrets scan (`api_key|API_KEY|hf_token|client_secret|aws_secret|BEGIN PRIVATE|sk-proj|ghp_` → NO hits in `src|scripts|config`); `password|passwd|secret` → YES locations-only: `compose.yaml:8` (`POSTGRES_PASSWORD` env-guard placeholder), `.gitignore:19` (`.env` ignored), `scripts/load_provenance.py:20` (+ siblings) local loopback `DEFAULT_DATABASE_URL` overridable via `LEGAL_XAI_DATABASE_URL`; `src/legal_xai/evidence_pipeline.py` takes `database_url` param (no hardcoded credential in `src/`). `.env` files: ABSENT (`Test-Path False`). Confidential legal data: corpus = public historical judgments; no private-client data found. Auth: none (local research tool; future deployment controls listed as required, not implemented). Privacy/audit-logging: run persistence (query/policy/rank/score) provides audit trail; no PII controls needed beyond public-record scope. Human-review requirement + uncertainty disclosure + citation verification + read-only demo: IMPLEMENTED (fail-closed exclusions, boilerplate uncertainty, verifier-v2, allowlisted static server).

SECRET FOUND: YES (local-only Postgres credential plumbing) | LOCATION: `compose.yaml:8`, `scripts/load_provenance.py:20` (+ env-override siblings) | ACTION REQUIRED: none for research baseline (do not commit `.env`; keep credentials env-only; no external secrets present). No external API keys/tokens/private keys found. No secret values printed in this report.

---

## 22. Scope Compliance Audit

Checked for: GraphRAG, multi-agent systems, multilingual core, production SaaS, large-scale prod infra, unrelated benchmarks, new RQs, unrelated model families — grep over `src/*.py` + `scripts/*.py` headers + `submission/MANIFEST.md`: **0 hits**, no out-of-scope additions found. Demo is static allowlisted server (no FastAPI/Flask/agents/LLM APIs/LangChain/AutoGen). All 62 script headers bounded to acquire/audit/build/check/compare/reconstruct/replay/retrieve/frozen-QA/validate/verify/serve-static/train-E1-E2. Verdict: repository stays within frozen scope. Table: none (no PATH/FEATURE rows to report). RECOMMENDATION: keep scope-freeze gates enforced (§4); route 75–100 key, blinded review, and hybrid retrieval through the specified separate-round/revision process rather than overwriting frozen assets.

---

## 23. Experimental Gaps

Based strictly on frozen spec (`submission/paper.md`, configs, checklist):

| GAP | WHY IT MATTERS | CURRENT STATUS | DATA/ASSET REQUIRED | CODE EXISTS? | HUMAN REQUIRED? |
|---|---|---|---|---|---|
| RQ1 facts-vs-evidence controlled comparison (E1/E2 vs E3/E4 prediction on same N) | tests whether grounding changes prediction, not just baselines side-by-side | BLOCKED — E1/E2 scored on N=1503; E3/E4 prediction on N=30 subset; cross-ref exists (`week12_prediction_cross_reference.json`: 30-subset 18/3/3/6) but no powered comparison | 30-subset E1/E2 slices exist; larger paired N needed | partial (cross-ref script) | no |
| RQ2 unconstrained-vs-controlled retrieval comparison | isolates causal contribution of pre-rank/salient/dedup bundle | PARTIAL — bounded 30-case post-rank vs pre-rank contrast exists (0.1667→0.40 @5; 0.40→0.50 @100) but verification bundle remains jointly tested (no single-variable ablation by design) | same 30 + frozen configs (present) | yes | no |
| RQ3 independent human evaluation | format claim currently rests on N=7 self-review | PENDING HUMAN DATA — infrastructure + packet + parity complete; 0 independent raters, 0 κ, non-random N=7 | 7 (or expanded) pairs + external raters + protocol | yes (packet + RQ3 scripts) | YES |
| Retrieval coverage (15/30 absent @100) | half the expected authorities never surface; caps RQ2 | BLOCKED on method — corpus contains misses (Week-9 spot: 5/5 misses corpus-present) → lexical/ranking limit, not temporal | hybrid dense-sparse or query/rank revision (future work) | no (retired configs only) | no |
| Answer-key coverage (30/40; era-skewed; single-authority) | n=30 underpowered; 43% 1980s; 138/150 nonmatches unlabeled | PARTIAL — 30 source-verified done; 10-case backlog | 10 era-balanced cases + multi-authority labels + nonmatch annotation | partial (validators exist) | YES (verification) |
| Multiple-authority evaluation | single ref understates valid retrieval (ceiling 0.20) | MISSING | multi-ref labels | UNKNOWN (no multi-ref schema found) | YES |
| Temporal P2 (exact-date) | year rule over-excludes same-year, under-specifies within-year order | OUT-OF-SCOPE by data constraint (ILDC year-only queries) | day-level ILDC dates (do not exist publicly) | no | no |
| Citation validity beyond grounding | 150/150 valid ≠ legally correct/relevant | MISSING by design (paper limits claim) | attorney relevance annotation | no | YES |
| Unsupported-claims beyond 0/150 | rate currently measured on displayed slots only | PARTIAL — 0/150 + 0/30 E3↔E4 splits + `correct-pred-unsupported 0` | broader claim-level annotation | partial | YES |
| Efficiency (latency/cost/index-build time) | prototype has no cost model | MISSING | timing harness | UNKNOWN | no |
| Ablations (single-component causal) | bundled verifier + bundled retrieval bundle | MISSING by design (paper §13.7) | ablation protocol + reruns (frozen-scope violation if done now) | no | no |
| Reproducibility (standalone) | external-asset + DB + CUDA + image needed | PARTIAL — local-asset model complete; standalone missing | Postgres up + CUDA + E2 image + asset hosting | yes (replay scripts) | no (ops only) |

---

## 24. Current-State Scorecard

| Area | Rating | Basis |
|---|---|---|
| research scope | COMPLETE | frozen RQs/protocols/exclusions documented + enforced |
| architecture | COMPLETE | all stages implemented with exact files (§3) |
| implementation | COMPLETE | src + scripts + demo present; no stubs found |
| datasets (ILDC) | COMPLETE | 5,082/994/1,517 present; 1,503 eligible frozen |
| corpus (eCourts) | COMPLETE | 39,069 PDFs / 2.34M chunks / 39,073 meta rows present |
| BM25 | COMPLETE | 2.27 GB FTS5 + temporal table present, 2,036,981 rows |
| provenance DB | PARTIAL | schema + loader + artifacts complete; live DB down here; no dump |
| E1 | COMPLETE | real, frozen, reproduced (0.6134/0.6123, N=1503) |
| E2 | COMPLETE | corrected real, frozen, reproduced (0.5968/0.5924, N=1503); 256-run discarded |
| E3 | COMPLETE (bounded) | real, frozen, reproduced; N=30 |
| E4 | COMPLETE (bounded) | real, frozen, reproduced; identical to E3 by design |
| RQ1 | COMPLETE | E1 vs corrected-E2 on N=1503 + comparison artifact |
| RQ2 | COMPLETE (bounded) | recovery + integrity on N=30/150; 15/30 absent disclosed |
| RQ3 | PENDING HUMAN DATA | packet + self-review done; independent review absent |
| retrieval evaluation | COMPLETE (bounded) | R@5/R@100/prec/rec/F1/ground/prov/temp/unsupported all reported N=30/150 |
| temporal integrity | COMPLETE (P1) | year pre-rank + rechecks + 0 violations; P2 out-of-scope by data |
| citation verification | COMPLETE (bounded) | 5-checks + run membership, 150/150, before+after render |
| explainability | COMPLETE | extract-only renderer + order + uncertainty + tests |
| human evaluation | PENDING HUMAN DATA | self-review only (7 cases, 1 author, 0 κ) |
| efficiency | MISSING | no timing/cost harness |
| ablations | OUT OF SCOPE | bundled-by-design per paper §13.7 |
| testing | PARTIAL | 75 pass; 2 files blocked on host (torch/transformers) |
| reproducibility | PARTIAL | freeze + replays PASS (local-asset model); standalone rerun needs external assets + services |
| governance | COMPLETE | fail-closed + disclosure + read-only demo + no secrets committed |
| demo | COMPLETE | 7-case static UI + parity checks + allowlisted server |

Ratings used: COMPLETE / PARTIAL / BLOCKED / PENDING HUMAN DATA / MISSING / OUT OF SCOPE / UNKNOWN — no UNKNOWN ratings required; all items evidenced.

---

## 25. Exact Remaining Work

TIER 1 — required before final empirical paper:

| TASK | WHY | DEPENDENCY | EXACT FILES | DATA/ASSET NEEDED | CODE EXISTS? | COMPLEXITY | IMPACT |
|---|---|---|---|---|---|---|---|
| Complete 10-case answer-key backlog (40 total, era-balanced) as SEPARATE round | raises n=30→40, reduces era skew, honors frozen-30 guard | source-verification protocol | `answer_key/authority_answer_key.json`, `authority_answer_key_manifest.md`, `scripts/validate_authority_answer_key.py`, `config/authority_answer_key_schema.json` | 10 ILDC test cases (post-1990s/2000s/2010s) + `scr.sci.gov.in` PDFs + verifier time | partial (validators) | medium (human-bound) | high (powers RQ2/RQ4, enables McNemar path) |
| Independent blinded RQ3 review + κ | converts self-review into human-subject evidence | frozen 7-pair (or expanded) packet | `artifacts/week13_review_packet.md`, `scripts/build_week13_rq3_review_packet.py`, `summarize_week13_review.py` | external raters + protocol + ratings | yes | medium (human-bound) | high (unlocks RQ3 claim) |
| Reconfirm test-suite green in E2/CUDA image (torch/transformers files) | closes host-only collection errors | E2 image + CUDA | `tests/test_e2_chunk_pool_windows.py`, `tests/test_evidence_augmented_prediction.py`, `docker/e2.Dockerfile` | E2 image build + GPU host | yes | low (ops) | medium (test completeness) |
| Bring Postgres up + re-verify run persistence from frozen artifacts | proves live provenance path, not just JSON | compose + dumps/loaders | `compose.yaml`, `scripts/load_provenance.py`, `scripts/build_bm25_index.py` | Docker + 2.3M-chunk load window | yes | medium (ops) | medium (DB-backed audit) |

TIER 2 — strongly recommended:

| TASK | WHY | DEPENDENCY | EXACT FILES | DATA/ASSET NEEDED | CODE EXISTS? | COMPLEXITY | IMPACT |
|---|---|---|---|---|---|---|---|
| Multi-authority + nonmatch relevance annotation (subset) | fixes ceiling-0.20/understatement + "138 unlabeled" caveat | attorney annotators | answer-key schema extension (new file; do not mutate frozen key) | relevance judgments | no (schema needed) | high (human) | high (retrieval validity) |
| Retrieval-failure analysis → bounded hybrid (dense-sparse) pilot WITH controls retained | addresses 15/30 absent @100 | current failure buckets | `src/legal_xai/retrieval.py`, `evidence_pipeline.py`, `config/evidence_selection.json` (new version, frozen v3 untouched) | embeddings + ablation protocol | no | high | high (RQ2) |
| Report CIs / paired tests on frozen Ns | quantifies uncertainty (esp. N=30) | frozen predictions | `artifacts/e1_e2_test_predictions.json`, `e2_test_predictions.json`, `e3_e4_*.json` | stats code only | partial | low | medium |
| Efficiency harness (index build, p50/p95 retrieval, E3/E4 inference) | paper-grade cost model | live services | new script (do not mutate frozen) | timed runs | no | low–medium | medium |

TIER 3 — optional engineering: per-file corpus hashes + manifest completion; diagnostic-CSV recovery (`dedup_alignment_rejections.csv`, `temporal_ambiguities.csv`); git-history restoration for transfer copy; hosted-asset + DB-backup publication; demo browser-verify in Edge/Playwright (script exists, not run here).

No new features proposed beyond frozen requirements (no GraphRAG/agents/multilingual/SaaS/models).

---

## 26. Recommended Next Sequence

1. Enforce transfer guard (no overwrite of frozen 30/artifacts) — `TRANSFER_README.md:5`.
2. Recruit independent RQ3 raters; run blinded review on frozen 7-pair packet; report κ (TIER 1, human path, longest lead time — start first).
3. In parallel, verify 10 backlog answer-key cases (era-balanced) as a separate round (TIER 1, human path).
4. Ops track: bring up Postgres (compose), reload provenance, rebuild nothing unless hashes mismatch; run full pytest inside E2/CUDA image to close 2 collection errors (TIER 1).
5. Recompute CIs/paired tests read-only from frozen predictions (TIER 2, no reruns).
6. Only then: pilot bounded retrieval improvements / multi-authority annotation as revision-stage work with new version IDs (TIER 2; never mutate frozen v-ids).
7. Refresh freeze as `-v5` ONLY when new human data lands; keep v4 artifacts immutable.

---

## 27. Evidence / File References

Core: `README.md`, `PROJECT_CHECKLIST.md`, `TRANSFER_README.md`, `TRANSFER_MANIFEST.json`, `compose.yaml`, `requirements.txt`, `pytest.ini`, `.gitignore`; `config/*.json` (16: `authority_answer_key_schema`, `citation_verification`, `datasets`, `e1_baseline`, `e2_baseline`, `e2_chunk_pool`, `e3_e4_evidence_augmented_prediction`, `evidence_selection`, `facts_extraction`, `grounded_answer`, `model`, `reproducibility_freeze`, `retrieval_qa_queries`, `week11_evaluation_round`, `week7_evidence_selection_queries`, `week8_grounded_answer_queries`); `src/legal_xai/*.py` (10 + init); `scripts/*.py` (84); `tests/*.py` (11); `answer_key/*` (3); `corpus/dataset_manifest.md`, `dedup_matches.csv`, `dedup_report.md`, `temporal_overlap_audit.md`, `ecourts/acquisition_record.json`, `ecourts/cleaning_record.json`; `retrieval/bm25.sqlite`; `artifacts/` frozen results (`e1_baseline_results`, `e2_chunk_pool_results`, `e2_baseline_results` (discarded), `e1_e2_comparison`, `e3_e4_evidence_augmented_evaluation`, `e3_e4_prediction_error_analysis`, `week11_*`, `week12_*`, `week13_*`, `week14_*`, `week15_*`, `week16_reproducibility_audit`, `week10_replay*`, `week9_answer_key*`, `bm25_index.json`, `provenance_load.json`, `ecourts_corpus_identity.json`); `demo/*`; `submission/paper.md`, `paper.html`, `paper.pdf`, `MANIFEST.md`, `figures/`; `docker/Dockerfile.ocr`, `docker/e2.Dockerfile`. Live verifications this audit: `pytest` (75 pass / 2 collection errors), `pip show` (torch/transformers absent), `Test-Path` (parquets/BM25/ckpt present; `.env`/`e2_model` absent), `git status` (no commits, transfer copy), DB/Docker down (service-unavailable, not asset-missing).

---

## FINAL REQUIREMENT — compact summary

CURRENT STATE:
NyayaTrace is a scope-frozen, fully implemented research prototype whose frozen empirical core (E1/E2 on N=1503; E3/E4 retrieval+integrity+prediction on N=30/150; year-granular temporal gate; 5-check citation verifier; 7-pair explanation packet with self-review; static 7-case demo; v4 reproducibility freeze with passing replays) is physically present and internally consistent, with retrieval coverage (15/30 absent), answer-key size/era (30/40, single-authority), and independent human evaluation as the explicit deferred items.

WHAT IS ACTUALLY COMPLETE:
E1 baseline (0.6134/0.6123, N=1503, real/frozen/reproduced); corrected E2 (0.5968/0.5924, N=1503, ckpt-6318 present, real/frozen/reproduced; 256-run discarded); E3/E4 retrieval (R@5 0.40, R@100 0.50) + integrity (150/150 grounded/provenance/eligible, 0 violations/unsupported) + prediction (0.6667/0.6032, N=30, E3==E4 by parity); P1 year-temporal gate (pre-rank + rechecks + tests); citation verifier (5 checks, before+after render); extract-only explanation renderer + static demo (7 cases, parity-checked); ILDC splits (7,593) + eCourts corpus (39,069 PDFs / 2.34M chunks) + BM25 index (2.04M rows, 2.27 GB) all physically present; freeze-v4 + replay contracts passing (local-asset model); governance (fail-closed, disclosure, read-only demo, no committed secrets); scope compliance (no GraphRAG/agents/multilingual/SaaS).

WHAT IS BLOCKED:
Full standalone rerun (needs Postgres up + CUDA + E2 image + gitignored large assets, all present-or-specified but services down/absent on this host); E2-predictor unit tests on bare host (torch/transformers missing — runnable in E2 image); P2 exact-date ordering (data constraint: ILDC query dates year-only); retrieval-coverage gains (lexical/ranking limit, corpus contains misses).

WHAT IS MISSING:
10-case answer-key backlog to reach 40 (era balance); independent blinded RQ3 review + agreement stats (only N=7 self-review exists); multi-authority + 138-nonmatch relevance labels; CIs/paired significance; efficiency harness; single-component ablations (out-of-scope by design); per-file corpus hashes + 2 gitignored diagnostic CSVs + DB dump + git history (transfer-copy gaps).

WHAT MUST BE DONE NEXT:
1. Start independent blinded RQ3 review on frozen packet (longest human lead time). 2. Verify 10 backlog answer-key cases as a separate round (do not overwrite frozen 30). 3. Bring up Postgres + rerun pytest inside E2/CUDA image to close ops gaps. 4. Compute CIs/paired tests read-only from frozen predictions. 5. Only then pilot bounded retrieval/multi-authority revision work under new version IDs + freeze v5 on new human data landing.

MOST IMPORTANT:
Do not modify the research system during this audit — accomplished (read-only except this report); treat v4-frozen assets as immutable and build all future work (human data first, retrieval/metrics second) on top, not over, this baseline.
