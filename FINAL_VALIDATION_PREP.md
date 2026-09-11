# Final Validation Preparation (no architecture change, no new research features)

Date (UTC): 2026-09-11. Basis: `FINAL_BASELINE_AUDIT.md` + read-only
re-verification performed in this phase. No frozen file was modified; no
experiment was run; no synthetic result was generated. New preparation-only
files live under `validation_prep/` (see its `README.md` for the guard rules).

Frozen preservation statement: E1/E2/E3/E4 results, the 30-case answer key
(`answer_key/authority_answer_key.json`, SHA `f4ccb0fa…00e81`), all frozen
configs/version IDs, and freeze v4 remain immutable. The CI engine reads
frozen per-case predictions and writes only to `validation_prep/`; the
extension workflow and RQ3 v3 kit are blank scaffolds (0 cases / 0 ratings).

---

## 1. Assets verified (physically present)

All present, sizes match freeze `bytes` where recorded: ILDC
`single_train/validation/test.parquet` (5,082 / 994 / 1,517 rows per freeze);
eCourts cleaned `71 × chunks.jsonl` (aggregate `f0229bbb…`, 2,343,435 records
per `artifacts/ecourts_corpus_identity.json`, whose aggregate hash verifies
OK); `retrieval/bm25.sqlite` (2,269,376,512 bytes); checkpoint-6318
(`model.safetensors` 437,958,648 bytes + `config.json` + `trainer_state.json`);
HF base cache blobs (2 × ~534 MB); `corpus/dedup_matches.csv`;
`src/legal_xai/` implementations (5/5 impl hashes OK); answer key (33 entries:
30 evaluation + 3 dev_example); E1 joblib; per-case prediction files
(E1/E2 1,503 records each; E3/E4 30 per-case records). No asset required for
replay was found missing. Absent by design (per TRANSFER_MANIFEST): PostgreSQL
dump (`provenance.dump`), `.env`/credentials, git history in this copy.

## 2. Hashes verified (25 freeze records checked with SHA-256 recomputation)

Method: `hashlib.sha256` over full file bytes vs `config/reproducibility_freeze.json`
(`final-reproducibility-freeze-v4-e3e4-prediction`); semantic cross-check of
all frozen metric values vs working-tree JSONs (all identical — see §7).

- OK (17): ILDC train/val/test; `facts_extraction.json`; `dedup_matches.csv`;
  `cleaning_record.json`; `bm25.sqlite`; E1 config + joblib; E2 config +
  result; ckpt-6318 weights/config/trainer_state; E3/E4 config; answer key;
  `compose.yaml`; all 5 `src/` impl files.
- BYTE-DRIFT, semantically equivalent (8): `corpus/dataset_manifest.md`
  (15337 vs 15355 B); `artifacts/ecourts_corpus_identity.json` (aggregate
  `f0229bbb…` identical; wrapper bytes differ); `artifacts/bm25_index.json`
  (semantic fields identical: 2,036,981 chunks, same bytes; embeds
  `built_at_utc`, so any rebuild changes bytes by design);
  `artifacts/e1_baseline_results.json` (metrics identical: 0.61344/0.612342,
  CM [[501,248],[333,421]], C=10.0, same splits/shas);
  `artifacts/e2_correction_manifest.json` (metrics identical);
  `artifacts/e3_e4_evidence_augmented_evaluation.json` (metrics identical:
  0.666667/0.603175, R@5 0.40/R@100 0.50, 150/150 integrity; per-case N=30);
  `artifacts/e3_e4_prediction_error_analysis.json` (categories identical);
  `docker/e2.Dockerfile` (320 vs 308 B = 12 B = line-ending delta;
  `.gitattributes` mandates LF, working tree carries CRLF on this file).
- Assessment: drift is consistent with LF↔CRLF normalization in this transfer
  copy plus timestamped rebuild metadata — NOT with metric or corpus change.
  Recommendation: normalize line endings / re-record byte counts in a v5
  freeze addendum at validation time; do NOT overwrite v4 or any artifact now.

## 3. Environment status

- Host: Python 3.13.14 (freeze records 3.11.9 — replay-only difference, noted);
  `scikit-learn 1.9.1`, `pyarrow 25.0.1`, `psycopg 3.3.5`, `pytest 9.1.1`,
  `rank-bm25 0.2.2` present. `torch` / `transformers`: ABSENT on host
  (verified `pip show` miss; 2 test files uncollectable on host, as audited).
- Docker: client 29.6.2 present; **daemon DOWN** (`docker ps` pipe error), so
  images were neither built nor run in this phase — E2-image contents below
  are verified from the pinned Dockerfile, not from a built image.
- E2 image definition (`docker/e2.Dockerfile`, content verified):
  `pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime` + `accelerate==1.0.1`,
  `pyarrow==18.1.0`, `scikit-learn==1.5.2`, `transformers==4.46.3`
  (training role; host replay role `transformers 5.15.0` per freeze — coexist
  by role, exact replay already demonstrated in Week 16).
- GPU: `nvidia-smi` WORKS on host (driver 596.08, CUDA 13.2 runtime); GPU
  compute inside the E2 container is UNKNOWN until the daemon is up and
  `docker run --gpus all` is tested. CUDA requirement for E3/E4 inference
  stands (`config/e3_e4_evidence_augmented_prediction.json`: cuda, fp16).
- Verdict: NO experiment run in this phase (environment-gated items above
  remain). Nothing was installed.

## 4. PostgreSQL status + exact restore/start commands

- Config (`compose.yaml`, hash OK): `postgres:16-alpine`
  (observed digest `postgres@sha256:cf78…20685`, server 16.15),
  container `legal-xai-postgres`, `127.0.0.1:54329:5432`, volume
  `legal_xai_postgres_data`, password via `${POSTGRES_PASSWORD:?…}` (no
  credential in repo; `.env` absent by design). Schema: `corpus_chunks`,
  `retrieval_runs`, `retrieval_results` (`scripts/load_provenance.py:22-63`).
- Status: service DOWN here (daemon down; `pg_isready` not on host PATH;
  connect refused). No dump exists (`provenance.dump` is a documented
  required-separate-transfer, never stored). Data loss: NONE presumed —
  `bm25.sqlite` + frozen JSONs intact; DB is rebuildable from cleaned corpus.
- Exact commands (validation machine, in order; preservation flags included):
  1. `$env:POSTGRES_PASSWORD = "<secret-from-operator>"` (never commit).
  2. `docker compose up -d postgres`
  3. `docker exec legal-xai-postgres pg_isready -U legal_xai -d legal_xai`
     (compose healthcheck covers this; expect healthy ≤ 60 s).
  4. Reload provenance WITHOUT touching the frozen record:
     `$env:LEGAL_XAI_DATABASE_URL = "postgresql://legal_xai:<pw>@127.0.0.1:54329/legal_xai"`
     `python scripts/load_provenance.py --corpus-root corpus --start-year 1950 --end-year 2020 --output validation_prep/provenance_reload.json`
     (default `--output` would overwrite frozen `artifacts/provenance_load.json` — always override as shown.)
  5. Verify-only index comparison (do NOT overwrite `retrieval/bm25.sqlite`):
     `python scripts/build_bm25_index.py --index validation_prep/bm25_verify.sqlite --output validation_prep/bm25_verify.json`
     then compare `chunks_indexed = 2036981` + SHA vs freeze `3187f7…`.
  6. Once loaded, create the missing dump for future transfers:
     `pg_dump -Fc -h 127.0.0.1 -p 54329 -U legal_xai -d legal_xai -f provenance.dump`
     (per TRANSFER_MANIFEST `required_separate_transfer`).

## 5. 40-case expansion status — WORKFLOW READY, 0/10 verified

- Deliverables (new, non-frozen): `validation_prep/answer_key_extension/EXTENSION_PROTOCOL.md`
  (separate-round rules, era targeting to dilute 1980s skew, per-case human
  verification mirrors Weeks 7–10, validation gate incl. frozen validator +
  10/10 alignment re-audit, informational-only retrieval spot check, v5
  addendum procedure) + `extension_template.json` (10 null slots, schema
  reference, frozen-30 SHA pointer; ZERO invented authorities/annotations).
- Frozen 30: untouched (hash re-verified OK this phase). No candidate IDs
  selected here — selection requires a human operator running
  `python scripts/check_answer_key_candidate.py --case-id <ID>` per candidate.
- Remaining: human source verification of 10 era-balanced ILDC test cases
  (2000s/2010s priority) + validator pass + alignment audit + freeze addendum.

## 6. RQ3 packet status — V2 RETAINED, V3 SPEC + BLANK READY, 0 ratings

- Existing (frozen, DB-dependent builder): `scripts/build_week13_rq3_review_packet.py`
  (seed 20260903, parity-enforced, reads `retrieval_runs`+`corpus_chunks` —
  requires §4 DB up; NOT rerun here), `artifacts/week13_review_packet.md`,
  `week13_review_response_template.json` (4 items/display + preference),
  `week13_rq3_ablation_parity.json` (7/7, 35/35 parity), self-review
  `week13_review_response_completed.json` (1 author, outside=false — retained
  separately, never merged).
- New (this phase): `validation_prep/rq3/RQ3_PACKET_SPEC.md` (blinded
  Display-1/2 labels, sealed coordinator key, frozen per-case order seed +
  per-reviewer case-shuffle seed, SIX 1–5 Likert items Q1–Q6
  clarity/finding-ease/trust/limits/navigation/overall-fitness + forced
  preference + notes, R01… enrollment with outside_reviewer=true, per-reviewer
  JSON response files, pre-registered stats) + `response_template_v3.json`
  (blank: `reviewers: []`, 0 ratings, no synthetic content).
- Agreement statistic: **Fleiss κ per item (primary, ≥3 raters) + percent
  agreement**, pairwise Cohen κ secondary, exact binomial test on preference,
  Wilcoxon signed-rank descriptive; case-level N=7, non-random — inference
  limited to sample (spec §6).
- Remaining: DB up + packet rebuild/cover sheets + ≥3 outside raters.

## 7. Confidence-interval implementation status — IMPLEMENTED + COMPUTED

- Engine (new): `validation_prep/confidence_intervals/compute_cis.py`
  (stdlib only; Wilson 95% for binomial rates; seeded bootstrap B=10,000,
  seed 20260911, percentile 2.5/97.5 for macro-F1; fail-closed freeze
  cross-check aborts on any point-estimate drift; refuses to write into
  `artifacts/`). Rerun: `python validation_prep/confidence_intervals/compute_cis.py`.
- Output (new, derived, provenance-stamped):
  `validation_prep/confidence_intervals/ci_results.json` (computed 2026-09-11;
  E4==E3 re-verified identical in-run). Headline 95% intervals:
  - E1 acc 0.6134 [0.5886, 0.6377] (922/1503); macro-F1 0.6123 [0.5879, 0.6367]
  - E2 mean-logit acc 0.5968 [0.5718, 0.6213]; F1 0.5924 [0.5668, 0.6169]
  - E2 majority acc 0.6015 [0.5765, 0.6259]; F1 0.5937 [0.5682, 0.6184]
  - E3/E4 acc 0.6667 [0.4878, 0.8077] (20/30); F1 0.6032 [0.4034, 0.7778]
  - R@5 0.40 [0.2459, 0.5768]; R@100 0.50 [0.3315, 0.6685]; precision 0.08 [0.0464, 0.1346]
  - Groundedness 1.0 [0.9750, 1.0]; provenance 1.0 [0.9750, 1.0];
    temporal-violation 0.0 [0.0, 0.0250] (rule-of-three ≤ 0.02);
    unsupported 0.0 [0.0, 0.0250]
- Reading note (descriptive, not a new test): E1–E2 accuracy/F1 intervals
  overlap substantially (consistent with frozen H1-not-supported); N=30
  intervals are wide by construction — always report with denominators.

## 8. Exact commands for the eventual real experiment run

Prerequisites: daemon up, `.env` secret set, GPU visible, E2 image built
(`docker build -f docker/e2.Dockerfile -t nyayatrace-e2 .`).

1. `docker compose up -d postgres` → pg_isready (§4.3) → §4.4 reload →
   `python scripts/build_bm25_index.py --index validation_prep/bm25_verify.sqlite --output validation_prep/bm25_verify.json` (compare-only).
2. Full tests incl. torch files (inside E2 image / CUDA host):
   `python -m pytest tests -q` (host covers 9 files; image must show all 11 collect).
3. Replay before any eval (compare-only, overwrites nothing):
   `python scripts/run_week10_reproducibility_replay.py`
   `python scripts/replay_e3_e4_evidence_augmented_evaluation.py`
4. E3/E4 evidence evaluation (CAUTION: default writes frozen
   `artifacts/e3_e4_evidence_augmented_evaluation.json` — back it up and/or
   confirm the run writes an exit-gated temp file; DO NOT `--force` until a
   v5-freeze decision is recorded): `python scripts/run_e3_e4_evidence_augmented_evaluation.py --help` first.
5. RQ3 packet rebuild (needs DB): `$env:LEGAL_XAI_DATABASE_URL=…; python scripts/build_week13_rq3_review_packet.py`
   then assemble v3 round per `validation_prep/rq3/RQ3_PACKET_SPEC.md` §7.
6. Extension validation (after 10 human-verified cases exist):
   `python scripts/validate_authority_answer_key.py` on frozen-30 + extension-10.
7. CI refresh (always safe, read-only): `python validation_prep/confidence_intervals/compute_cis.py`.
8. Demo (read-only): `python scripts/serve_week16_demo.py --port 8000`.

## 9. Remaining human/data dependencies (nothing else blocks)

1. HUMAN: 10-case source verification (era-balanced) — owner: legal verifier; blocks 40-case metrics + McNemar path.
2. HUMAN: ≥3 independent outside reviewers + round coordination (keys, cover sheets, receipt log) — blocks RQ3 claim.
3. OPS: Docker daemon + GPU passthrough + Postgres reload (§4) — blocks live replay/RQ3 rebuild/index-verify.
4. OPS: E2 image build + full-suite green — blocks torch-file test closure.
5. DATA: `provenance.dump` creation on first load (future transfers).
6. DECISION: v5 freeze-addendum trigger (after 1 and/or 2 land) + line-ending normalization record for the 8 drifted bytes (§2).

Most important: everything committable to validation now is prepared without
touching frozen state; the critical path is human data (extension cases,
independent ratings) behind ops restoration (DB/GPU), in that order.
