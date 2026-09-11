# Final Baseline Reproduction Report — NyayaTrace (execution + validation only)

Date (UTC): 2026-09-11. No features added, no architecture/redesign/refactor,
no RQ/scope/definition/config changes, no retraining, no tuning, no
substitutes, no fabrication, no synthetic results. All regenerated outputs are
under `validation_replay/`; no frozen artifact was overwritten (verified §2).

Scope respected throughout: primary = evidence-grounded Indian legal
research; secondary = historical outcome prediction; BM25 core baseline;
grounding + provenance/citation verification + temporal eligibility +
structured explanation + required human review. Nothing autonomous, no
GraphRAG/agents/multilingual-core/SaaS/benchmarks/new RQs (§14).

STOP observed: no 40/75–100-case eval, no RQ1/RQ2/RQ3 final eval, no hybrid
comparison/ablations/tuning/training/reviewer evaluation.

## 1. Executive Summary

The repository faithfully reproduces its frozen baseline. Environment was
brought online from repo definitions only (Docker daemon now up; PostgreSQL
16.15 started via `compose.yaml`; provenance reloaded with byte-identical
counts 2,343,435 → 2,036,981 + 306,454 skipped; E2 image built from
`docker/e2.Dockerfile` with GPU passthrough to the RTX 3050). Results:
**E1 EXACT** (C=10.0, 0.61344/0.612342, CM identical, N=1503);
**E2 EXACT** (checkpoint gate passed; 0.596806/0.592358 + vote 0.601464/0.593682,
all 1,503 per-case predictions identical); **E3/E4 41/42 metrics EXACT**
(R@5 0.40, R@100 0.50, precision 0.08, 150/150 integrity, 0 violations,
0 unsupported, 0.666667/0.603175, CM [[4,3],[7,16]]) with **1 MINOR
logits-only drift** (~1e-4, torch/cuDNN across environments, zero metric
impact, root-caused). Tests **81/81 pass** (75 host + 6 container, 0 failures).
Freeze: 22 EXACT_MATCH + 8 BYTE_DRIFT (all root-caused, semantics identical),
0 missing. Verdict: **READY** (RQ1/RQ2/RQ3 remain unanswered by design — next phase).

## 2. Repository Baseline

- Repository root: `C:/Users/uvi58/OneDrive/Documents/NyayaTrace` (confirmed via `Get-Location` + `git rev-parse --show-toplevel`).
- Commit hash: NONE — `git rev-parse HEAD` fails; branch `main` has no commits yet; all files untracked (transfer copy). Upstream reference only: TRANSFER_MANIFEST `source_commit 75da550dcf2a9057782be194f0631d09ea22c945` (history not present here).
- Git status: `## No commits yet on main...origin/main [gone]` + untracked entries (full snapshot).
- Frozen-file changes by THIS phase: NONE. Re-verified post-run SHAs: answer key `f4ccb0fa…` (matches freeze), E2 result `d68be6…` (matches freeze), E1/E3E4 files byte-identical to their pre-phase values from the prep audit (pre-existing drift unchanged).
- Execution record: `validation_replay/baseline_execution_metadata.json` (created Phase 0; lists all frozen no-overwrite paths; outputs confined to `validation_replay/`).
- Frozen no-overwrite areas (all honored): E1/E2/E3-E4 result files, 30-case answer key, `config/`, freeze v4, paper/result artifacts, BM25 index, ILDC splits, checkpoint.

## 3. Asset Verification

A. ILDC (revision `d16219ad0423cc181ec8460d930fd10a907664b6` per `config/datasets.json`; canonical name `single_validation.parquet` preserved):
`single_train.parquet` 56,421,032 B / 5,082 rows / 8 cols (`id,text,label,expert_1..5`) / SHA `0d878a…884f4b3` readable; `single_validation.parquet` 10,770,658 B / 994 / same cols / `2140d5…ca8fa1`; `single_test.parquet` 16,839,899 B / 1,517 / same cols / `10cddb…0a36efc`. All match expected hashes.
B. eCourts: 71/71 cleaned year dirs (1950–2020, 0 missing), 2,343,435 chunk records, 2,712,095,037 cleaned bytes; 71 metadata parquets, 39,073 rows; 39,069 PDFs (~21.0 GB); `dedup_matches.csv` 386,115 B; manifest + identity present (aggregate `f0229bbb…`). No rebuild performed.
C. BM25 `retrieval/bm25.sqlite`: 2,269,376,512 B, readable; tables `chunks_fts(+_config/_content/_data/_docsize/_idx)` + `chunk_temporal_metadata`; 2,036,981 rows each; years 1950–2020; SHA `3187f7…350d65fb` (matches). No rebuild/replace.
D. Checkpoint-6318: `model.safetensors` 437,958,648 B SHA `924a5b…dc773` (matches); `config.json` (bert/BertForSequenceClassification) 760 B; `trainer_state.json` 12,931 B; `training_args.bin` 5,304 B; no tokenizer files in ckpt dir (tokenizer resolved from `e2_hf_cache` hub blobs at runtime). No retrain/replace.
E. Answer key: 33 entries = 30 evaluation + 3 dev_example; 17 schema fields incl. source URLs, both dates, `independent_of_system_retrieval` (all true), relationships, `temporal_status`; query years 1971–2013; manifest present; SHA `f4ccb0…00e81` (matches). NOT expanded (30 frozen).
F. Config: 16 files in `config/`; freeze `final-reproducibility-freeze-v4-e3e4-prediction`.
G. Result artifacts (all classified **executed result**, none fixture/synthetic/docs-only): E1 (split SHAs + env versions + selection protocol + per-case predictions present); E2 (window coverage 9,576 + checkpoint-gated inference + per-case records); E3/E4 (30 per-case records with run UUIDs + raw logits + citation checks). Verdict basis: deterministic provenance chains + exact replay gates + this phase's successful re-execution.

## 4. Hash Verification

Full table: `validation_replay/freeze_validation.json`. Summary: **22 EXACT_MATCH, 8 BYTE_DRIFT, 0 MISSING, 0 UNKNOWN**. Every BYTE_DRIFT root-caused as metadata/timestamps/line-endings/generated-bytes with semantic content verified identical (manifest line endings; identity wrapper vs identical aggregate; `bm25_index.json` embeds `built_at_utc` by design; E1/E3E4/correction/error-analysis JSON re-serializations with identical metrics; Dockerfile 12 B CRLF delta). v4 artifacts NOT overwritten. Rule applied: never modify files to force hashes.

## 5. Environment Verification

| Component | Status | Evidence |
|---|---|---|
| Docker client | OK | 29.6.2, windows/amd64 |
| Docker daemon | OK (was down in prep audit, up now) | `docker ps` works; Desktop 4.83.0/Engine 29.6.2 |
| Docker Compose | OK | v5.3.1; `compose.yaml` used unmodified |
| GPU visibility | OK | host `nvidia-smi` (driver 596.08, CUDA 13.2) |
| NVIDIA passthrough | OK | `--gpus all` → `cuda_avail True`, RTX 3050 6GB Laptop GPU |
| CUDA (torch) | OK in E2 image | torch 2.5.1+cu124 |
| Python | OK | host 3.13.14 (freeze records 3.11.9 — replay-only note); image 3.11 |
| PyTorch | OK in image / absent on host | image 2.5.1+cu124 (frozen training env); host absent by design |
| Transformers | OK in image / absent on host | image 4.46.3 (frozen training role; replay role 5.15.0 per freeze) |
| PostgreSQL | OK | 16.15 via compose (matches freeze observed) |
| sklearn/pyarrow/psycopg | OK | host 1.9.1/25.0.1/3.3.5; image 1.5.2/18.1.0 + runtime-added psycopg 3.3.4 + rank-bm25 0.2.2 (pinned, container-only) |

No Dockerfile/dependency changed; no arbitrary packages. Image-only additions (pytest 9.1.1, psycopg 3.3.4, rank-bm25 0.2.2) are pinned test/DB plumbing, not version substitutions.

## 6. PostgreSQL Verification

Compose service `postgres` (container `legal-xai-postgres`), db `legal_xai`, user `legal_xai`, port `127.0.0.1:54329→5432`, volume `legal_xai_postgres_data`, password via env (never printed). Started with existing config only. Fresh volume → schema created by repo loader: `corpus_chunks`, `retrieval_runs`, `retrieval_results` (+ date/source indexes). Counts after sanctioned reload: `corpus_chunks` **2,036,981** (expected), `retrieval_runs` 0 → 30 after E3/E4 replay (expected side effect, new UUIDs), `retrieval_results` 3,000 (30×100). Reload output: `validation_replay/provenance_reload.json` (2,343,435 read / 2,036,981 unique / 306,454 skipped — identical to frozen record). No dump existed and none was needed (rebuild path used); dump-creation command recorded for next phase. No dummy tables/data; no credentials exposed.

## 7. Full Test Results

`python -m pytest tests/ -q`: host → **75 passed**, 2 collection errors (`test_e2_chunk_pool_windows.py`: no `transformers`; `test_evidence_augmented_prediction.py`: no `torch`) — both ENVIRONMENT_BLOCKED (host lacks DL libs by design), none code-related. In E2 image (pytest 9.1.1 installed at runtime): **6 passed**. Total **81/81, 0 FAIL, 0 code-related**. Per-module: 9 host modules PASS (incl. temporal/retrieval/citation-verifier/grounded-answer/evidence-pipeline/facts/corpus/alignment/answer-key); 2 DL modules PASS in image, ENVIRONMENT_BLOCKED on host. No test modified. Research impact: none — full contract coverage green in the appropriate environments.

## 8. E1 Frozen Reproduction — EXACT_REPRODUCTION

Original split/config/seed/implementation only (`config/e1_baseline.json`, seed 202605, C∈{0.1,1,10}); outputs to `validation_replay/e1/` (`--output-json/--output-markdown` redirect; frozen files untouched). Population N: train 5,020 / val 983 / test 1,503 eligible (excl 62/11/14); test labels 0:749/1:754. Selected C=10.0. Accuracy **0.61344**, Macro-F1 **0.612342**, C0 0.632975/C1 0.591708, CM [[501,248],[333,421]], majority-1 baseline 0.501663 (+11.1777pp) — all bit-identical to frozen. Runtime: host sklearn 1.9.1 (freeze 1.9.0) — no numerical impact observed. No tuning; no implementation change.

## 9. E2 Frozen Reproduction — EXACT_REPRODUCTION

No retraining: cache regenerated deterministically (`prepare_e2_chunk_pool_cache.py` → `validation_replay/e2_cache/`: 5,020→33,702 / 983→6,054 / 1,503→9,576 windows — matches frozen coverage; tokenizer = pinned `b5ecfed8` revision) then frozen-checkpoint inference (`infer_e2_checkpoint_predictions.py`, CUDA, batch 2) with its built-in exact gate (aborts + writes nothing on any metric mismatch — gate PASSED, output written). Checkpoint hash `924a5b…` verified; 512 length / 50 overlap / mean-logit primary + majority-vote (lower-label ties) confirmed. Mean-logit **0.596806/0.592358** CM [[527,222],[384,370]]; vote **0.601464/0.593682** CM [[556,193],[406,348]]; all 1,503 per-case predictions identical to frozen. Output: `validation_replay/e2/e2_reproduced_predictions.json` (213,928 B — same size as frozen). Checkpoint NOT replaced.

## 10. E3/E4 30-Case Evidence Reproduction — EXACT (41/42) + 1 MINOR

Original frozen configuration only (30-case key enforced `len==30`; frozen BM25/corpus/dedup/temporal/k100/top-5/renderer/verifier/provenance; `--output` redirect; no expansion, no variants). Retrieval: R@5 **0.40** (12/30), R@100 **0.50** (15/30). Authority: P **0.08** (12/150), R 0.40, F1 0.133333. Integrity: groundedness **1.0**, provenance **1.0**, temporal-violation **0.0**, unsupported **0.0** (150/150; 0/150). Prediction: E3=E4 **0.666667/0.603175** CM [[4,3],[7,16]] (parity check passed in-run). Populations: 30 cases / 150 citations / 3,000 candidates; error-analysis categories re-derivable unchanged. Output: `validation_replay/e3_e4/e3_e4_reproduced_evaluation.json`. Frozen artifacts untouched.

## 11. Metric-by-Metric Comparison

Machine-readable: `validation_replay/metric_comparison.json` — **41 EXACT_REPRODUCTION + 1 MINOR_NUMERICAL_DRIFT, 0 MATERIAL_DRIFT, 0 BLOCKED** (columns: experiment/metric/frozen/reproduced/difference/population/status/explanation). The single non-exact row (`E3/E4 per_case_stable_records`, run-UUID-excluded) is logits-only: 5/30 cases differ in raw `mean_logits` at ~1e-4 with labels, ranks, citations, provenance all identical (see §12).

## 12. Drift Investigation

Two drift classes, both resolved without touching the system: (a) 8 pre-existing BYTE_DRIFTs — line endings (`Dockerfile`, manifest), embedded build timestamps (`bm25_index.json`), JSON re-serialization (result files) — semantics verified identical, and E1/E2/E3-E4 re-execution now independently confirms the numbers; (b) raw-logit ~1e-4 differences in 5/30 E3/E4 cases — cause: torch/cuDNN kernel nondeterminism across environments (frozen inference: torch 2.13.0+cu130 host replay; this reproduction: torch 2.5.1+cu124 E2 image), evidenced by identical argmax/labels/metrics with only float tails differing. No MATERIAL_DRIFT; nothing unknown outstanding.

## 13. Fixture/Synthetic Contamination Check

`validation_replay/` scanned for `FIXTURE|SYNTHETIC|PLACEHOLDER|MOCK|ESTIMATED`: **0 hits**. All replay outputs derive from frozen inputs via frozen code paths (train/infer/eval scripts with provenance gates). Frozen results, empirical tables, and conclusions draw only from executed reproductions above. Contamination: NONE.

## 14. Research-Scope Compliance

Confirmed in current tree: primary = Indian legal research/evidence-backed analysis; prediction secondary with separate top-level field + non-advice boilerplate; BM25 is the core baseline (FTS5; no dense/hybrid code found); grounding, provenance/citation verification, temporal pre-rank + rechecks, structured extract-only explanation, and required human review all implemented and exercised. English core, local research scale. Absent as required: autonomous decisions/judge/lawyer behavior, GraphRAG, multi-agent reasoning, multilingual core, production search/SaaS, unrelated benchmarks, new RQs, chain-of-thought exposure (grep over `src/*.py`: 0 hits). `validation_prep/` + `validation_replay/` additions are audit scaffolding, not architecture. Concern: NONE.

## 15. Reproducibility Assessment

From repo + repo-defined services alone: ILDC splits ✓, corpus ✓, BM25 ✓ (hash-exact), checkpoint ✓, answer key ✓, configs ✓, code ✓, PG reload ✓ (counts-exact), E1/E2/E3-E4 re-execution ✓ (41 exact + 1 minor). Replays used only sanctioned scripts with outputs redirected. Remaining non-hermetic notes (accepted, documented): GPU + Docker required for E2/E3-E4; torch minor-version float tails (~1e-4, metric-neutral); transfer copy carries no git history; no PG dump existed (rebuild path proven; dump command staged).

## 16. Remaining Blockers

NONE for the baseline. Explicitly NOT blockers: 8 byte-drifts (resolved), logits tails (resolved), host-missing torch (image path proven), empty-then-loaded DB (loaded + verified). Next-phase (out-of-scope here) dependenciesGov: 10 extension cases + independent raters (human), PG dump creation (ops), v5 addendum decision.

## 17. Exact Commands Executed

Pre-flight/inventory: `git rev-parse --show-toplevel`, `git rev-parse HEAD` (no HEAD), `git status --porcelain=v1 --branch`, hash/row/table inspection scripts (`verify_hashes.py`, `phase1_inventory.py`, `semantic_check*.py`, `pred_schema.py`, `e2keys.py`, `e3keys.py` — temp dir, read-only). Env: `docker version`, `docker compose version`, `docker ps`, `nvidia-smi`, host `pytest` runs. DB: `docker compose up -d postgres` (repo-default local credential via env), `docker exec legal-xai-postgres pg_isready -U legal_xai -d legal_xai`, `python scripts/load_provenance.py --corpus-root corpus --start-year 1950 --end-year 2020 --output validation_replay/provenance_reload.json`. Tests: `python -m pytest tests/ -q` (+ `--ignore`s for scoped run; `--co` for counts). E1: `PYTHONPATH=src python scripts/train_e1_baseline.py --config config/e1_baseline.json --output-json validation_replay/e1/e1_reproduced_results.json --output-markdown validation_replay/e1/e1_reproduced_results.md`. Image: `docker build -f docker/e2.Dockerfile -t nyayatrace-e2:repro .`; `docker run --rm … python -c torch/transformers versions`; `docker run --rm --gpus all … cuda check`; container pytest after `pip install -q pytest==9.1.1`. E2: container `prepare_e2_chunk_pool_cache.py --config config/e2_chunk_pool.json --cache-dir validation_replay/e2_cache`; container `infer_e2_checkpoint_predictions.py --cache-dir validation_replay/e2_cache/test --checkpoint artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318 --recorded-result artifacts/e2_chunk_pool_results.json --output validation_replay/e2/e2_reproduced_predictions.json --batch-size 2`. E3/E4: container `run_e3_e4_evidence_augmented_evaluation.py --output validation_replay/e3_e4/e3_e4_reproduced_evaluation.json --database-url postgresql://legal_xai:<repo-default-local-pw>@host.docker.internal:54329/legal_xai` (after `pip install -q 'psycopg[binary]==3.3.4' rank-bm25==0.2.2`). Analysis: `metric_compare.py`, `percase_diff.py`, `patch_row.py`, `freeze_val.py`, `final_checks.py`, `validation_prep/confidence_intervals/compute_cis.py` (prior phase, read-only).

## 18. Exact Commands Required for Next Phase

regen-verify: rerun §17 replay commands (never with frozen `--output` defaults; keep `--force` OFF unless a v5 decision is recorded). DB dump (still missing, create once): `pg_dump -Fc -h 127.0.0.1 -p 54329 -U legal_xai -d legal_xai -f provenance.dump`. Extension (after 10 human-verified cases): `python scripts/check_answer_key_candidate.py --case-id <ID>` per candidate; `python scripts/validate_authority_answer_key.py` on frozen-30 + extension-10. RQ3: set DB URL then `python scripts/build_week13_rq3_review_packet.py` + `validation_prep/rq3/RQ3_PACKET_SPEC.md` round procedure. Teardown if needed: `docker compose stop postgres` (leave data volume; do NOT `down -v`). Next phase must NOT start 40/75–100/RQ/diagnostic experiments until its own authorization.

## 19. Final Readiness Verdict

Required components reproduced: E1 exact; E2 exact (checkpoint-gated); E3/E4 30-case exact incl. retrieval/authority/integrity/prediction populations; tests 81/81; assets + freeze + DB + scope all verified with zero unresolved integrity issues and zero frozen overwrites.

BASELINE REPRODUCTION STATUS:
READY

(Declared strictly as baseline fidelity. RQ1/RQ2/RQ3 are NOT answered; no 40/75/100-case claim is made; E3-vs-E1/E2 cross-population comparison remains disallowed per §9 population separation.)
