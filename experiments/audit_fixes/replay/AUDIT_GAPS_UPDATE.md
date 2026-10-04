# Audit verification gaps — progress update (2026-09-28)

##69943b34 Closed with evidence

### E1 repeated deterministic replay — CLOSED
- `docker run ... python experiments/audit_fixes/scripts/e1_canonical_diff.py`
- Output:
  - `canonical hash run1: d719f1d983bddbaf7516214e176d527f5060229da71e60b7869a01d2ca249042`
  - `canonical hash run2: d719f1d983bddbaf7516214e176d527f5060229da71e60b7869a01d2ca249042`
  - `canonical JSON: IDENTICAL`
  - `metrics: IDENTICAL`
  - `prediction arrays length: run1=1503 run2=1503`
  - `prediction arrays: IDENTICAL`
  - `all other keys: IDENTICAL`
- Files: `experiments/audit_fixes/replay/e1_test1.json`, `e1_test2.json` (hashes 1F4CD..., 0218E... differ only in `model_artifact` path field).

### E2 replay — CLOSED (exact reproduction)
- Checkpoint: `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318`
  - `model.safetensors` sha256 `924a5bb9078bcc212ef07acb9f08dfaa8593e880ae3868203deb28586dbdc773` (via `sha256sum` in container)
  - Matches `config/e3_e4_evidence_augmented_prediction.json` and frozen E2 record.
- Config: `config/e2_chunk_pool.json` sha256 `633C0E3E...` matches `artifacts/e2_chunk_pool_results.json:config_sha256`.
- Test population: train 5020 docs / 33702 windows, validation 983 / 6054, test 1503 / 9576 (from `e2_cache_prep.log`, matches frozen).
- Environment: CUDA RTX 3050 6GB Laptop GPU, driver 616.92, torch 2.5.1+cu124, transformers 4.46.3, sklearn 1.5.2, pyarrow 18.1.0 base (21.0.0 installed for replay per log), psycopg 3.3.4.
- Metrics (replay `experiments/audit_fixes/replay/e2_test_predictions.json`):
  - accuracy 0.596806, macro_f1 0.592358, class_0_f1 0.63494, class_1_f1 0.549777, CM [[527,222],[384,370]], records 1503.
  - File hash identical to frozen `artifacts/e2_test_predictions.json` (`3A27FD...` both).
  - `records identical: True` via container JSON compare.
- Log: `experiments/audit_fixes/replay/logs/e2_inference.log` → `exact_reproduction_confirmed`.
- Repeat (determinism + timing, log `e2_repeat2.log`): second run `exact_reproduction_confirmed`, wall 89.5s (`time -p real 89.58`), max RSS 1214 MB, repeat-vs-first records `identical: True`, metrics `identical: True`. Output `e2_test_predictions_repeat.json`.

### Test suites — CLOSED
- Pytest: `81 passed in 6.33s` (`experiments/audit_fixes/replay/logs/pytest.log`).
- FastAPI: `6 passed` (`experiments/audit_fixes/replay/logs/fastapi_tests.log`).
- Spring: `Tests run: 8, Failures: 0, Errors: 0, Skipped: 0`, `BUILD SUCCESS` in `experiments/audit_fixes/replay/logs/spring_retest.log`
  - `MlClientContractTest: Tests run: 1`
  - `ResearchControllerTest: Tests run: 7`.

### Machine environment — CLOSED (correctly labeled)
- Host: Windows, 13th Gen Intel i5-13450HX (10 cores / 16 logical), 16GB RAM (16454352 KB total).
- Docker: Server 29.8.0, CPUs 16, MemTotal 8161751040, OSType linux, Arch x86_64.
- Linux container: `nproc=16`, `MemTotal 7970460 kB` via `/proc/meminfo` (slim image has no `free`; do not report Windows values as `free -m`).
- GPU host + inside CUDA container: `NVIDIA GeForce RTX 3050 6GB Laptop GPU, 616.92, 6144 MiB` via `nvidia-smi`.
- Uname: `Linux ... 6.18.33.2-microsoft-standard-WSL2`.

### Security — ROTATED
- Old DB password (exposed in prior command history) rotated via `ALTER USER` without secrets in logs.
- New URL in gitignored `experiments/audit_fixes/replay/.db_env` (132 chars, encoded), used via `docker --env-file` (no plaintext in commands).
- Verified: new URL connects (`corpus_chunks count=2036981`), old URL rejected (`OperationalError`).
- Repo scan: no `audit2026rotated` in tracked files; `experiments/audit_fixes/replay/logs/*` clean.
- Do not put credentials in paper/report. Removed temp helpers; kept only `.db_env` (gitignored).

### Retrieval leakage / self-match — AUDITED (top-5)
- Script: `experiments/audit_fixes/scripts/leakage_audit.py` → `experiments/audit_fixes/replay/leakage_audit.json`.
- Result: eval_n 30, missing 0, queries_with_dedup_exclusion 16/30, queries_with_self_in_top5 0/30, temporal_violations 0.
- Frozen Recall@5 0.4, Recall@100 0.5, provenance 1.0, groundedness 1.0.
- Metric is authority recall, not query recall; self-match excluded by dedup + 100-phrase/80%-coverage direct-content rule + strict earlier-year preranking.
- Still pending: top-100 candidate-level self-match via `retrieval_runs`/`retrieval_results` after successful E3/E4 replay (DB currently 0 runs).

## In progress

### BM25 rebuild — CLOSED
- Frozen `artifacts/bm25_index.json` vs rebuilt `experiments/audit_fixes/replay/bm25_rebuilt.json`: chunks 2036981 MATCH, version/engine/tokenizer MATCH, bytes 2269376512 MATCH (only timestamp/path differ).
- Deep compare (`bm25_deep_compare2.py`, log `bm25_deep_compare2.log`, result `bm25_deep_compare.json`): ordered chunk_id SHA `4d294043...` both → `chunk_identity: IDENTICAL`; production temporal+salient_tfidf top-100 over 30 eval queries → 30/30 `MATCH`, `overall_ranking: MATCH`.
- Raw SQLite SHA differs (`3187F7...` vs `F2A70B...`) — internal pages only; behavior identical. Old 0-query probe bug fixed.

### E3/E4 replay — running on CUDA
- Frozen: n=30, E3/E4 accuracy 0.666667 macro_f1 0.603175 CM [[4,3],[7,16]], Recall@5 0.4 Recall@100 0.5 provenance 1.0.
- Prior failures: no `--gpus` (CUDA check) and read-only `HF_HOME`. Fixed: `--gpus all`, writable `/hf_cache` (`experiments/audit_fixes/replay/e2_hf_cache`), `HF_HUB_OFFLINE=1`.
- Background: `run_e3e4_replay.sh` in `nyayatrace-e2` with `--env-file .db_env` running; log `e3e4_replay_gpu2.log` shows BERT windowing warnings (inference in progress).
- NOTE 20:52 UTC: gpu2 run failed mid-flight because DB password was rotated underneath it (`password authentication failed` after `ALTER USER`). Relaunched as gpu3 with the new `.db_env` (no further rotations). Log `e3e4_replay_gpu3.log`.
- RESULT gpu3 (completed, exit 1 on strict hash but metrics recomputed from source): E3 acc 0.666667 macro_f1 0.603175 CM [[4,3],[7,16]] MATCH; E4 identical MATCH; evidence Recall@5 0.4 Recall@100 0.5 provenance 1.0 groundedness 1.0 temporal 0.0 MATCH. Strict stable-hash (excl. only `retrieval_run_id`) MISMATCH (ref 852b... vs replay 6f5f...) — under diagnosis; ordering/keys/config all verified identical, no stray `run_id` keys, UUIDs exactly 30. Direct rerun to persistent `/out/e3e4_replay.json` launched (log `e3e4_direct.log`) for field-level diff + per-case Recall verification.
- ROOT CAUSE (from `/out/e3e4_replay.json` diff): GPU fp16 nondeterminism in `mean_logits` only. `input_sha256` identical (retrieval deterministic), `predicted_label` 30/30 identical, selected chunk_ids 30/30 identical, per-case Recall 12/30 + 15/30 + selected 12/30 identical, E3==E4 parity holds. Max abs logit diff 0.00076723 — does not affect argmax. Verdict: recomputed from source, functionally exact; strict hash mismatch is fp16 noise, not a decision/metric difference. Scripts: `diff_e3e4.py`, `verify_e3e4_functional.py`.
- On success: verify per-case Recall 12/30 and 15/30 from raw outputs, not just aggregates.

## Still pending after background tasks
- BM25 deep compare result → final verdict.
- E3/E4 PASS with stable_sha256 → per-case verification.
- E2 repeat with `/usr/bin/time -v` for wall/RSS + determinism (needs GPU free).
- Top-100 self-match via DB runs.
- Plagiarism audit, paper claim/evidence mapping (do not start until BM25/E2/E3E4 closed).
