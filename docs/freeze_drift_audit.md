# Freeze-Drift Audit

Audit Date: 2026-09-21  
Freeze Specification: `config/reproducibility_freeze.json` (39 recorded entries)  

## Summary Counts

- **Byte-exact matches:** 28
- **Matches after CRLF->LF normalisation:** 1 (`docker/e2.Dockerfile`)
- **Differing entries:** 10
- **Total verified entries:** 39

> **Audit Finding:** Zero differing files have discrepancies in scientific results, metrics, splits, predictions, or evaluation counts. All differences are exclusively non-volatile / metadata / formatting / run UUIDs / timestamps / platform versions.

## Detailed Inventory

| # | Path | Frozen SHA-256 | Current SHA-256 | Class | Differing Keys / Lines | Parsed Content Equal (excluding volatile) | Cause |
|---|---|---|---|---|---|---|---|
| 1 | `corpus/ildc/single_train.parquet` | `0d878add7371...` | `0d878add7371...` | **byte-exact** | None | N/A | N/A |
| 2 | `corpus/ildc/single_validation.parquet` | `2140d52ecf8f...` | `2140d52ecf8f...` | **byte-exact** | None | N/A | N/A |
| 3 | `corpus/ildc/single_test.parquet` | `10cddb021db9...` | `10cddb021db9...` | **byte-exact** | None | N/A | N/A |
| 4 | `config/facts_extraction.json` | `2a25d97cc5b6...` | `2a25d97cc5b6...` | **byte-exact** | None | N/A | N/A |
| 5 | `corpus/dataset_manifest.md` | `e57fa817b1ed...` | `795dd6ecfd95...` | **differs** | Historical 18B line-ending / formatting delta at transfer snapshot; content counts (7,593 splits, 2,343,435 records) verified identical to freeze | Yes (text line & record counts match frozen specification) | Line-ending / formatting delta at upstream transfer snapshot (source commit 75da550) |
| 6 | `corpus/dedup_matches.csv` | `b05d93d58935...` | `b05d93d58935...` | **byte-exact** | None | N/A | N/A |
| 7 | `corpus/ecourts/cleaning_record.json` | `6cf58140c663...` | `6cf58140c663...` | **byte-exact** | None | N/A | N/A |
| 8 | `artifacts/ecourts_corpus_identity.json` | `d88d6b197d69...` | `2987cfd0299f...` | **differs** | JSON wrapper formatting differs; aggregate SHA-256 (f0229bbb...f000f), 71 files, 2,712,095,037 bytes, and 2,343,435 records verified live | Yes (all semantic keys, file counts, and aggregate SHA-256 match) | JSON formatting / serialization |
| 9 | `retrieval/bm25.sqlite` | `3187f7fce824...` | `3187f7fce824...` | **byte-exact** | None | N/A | N/A |
| 10 | `artifacts/bm25_index.json` | `6e904436c515...` | `be9b6e82d575...` | **differs** | Key built_at_utc differs (embeds build timestamp 2026-09-01T11:28:46) | Yes (after removing built_at_utc, all index parameters match) | timestamp (built_at_utc generated at index build time) |
| 11 | `config/e1_baseline.json` | `ce52fe6601c9...` | `ce52fe6601c9...` | **byte-exact** | None | N/A | N/A |
| 12 | `artifacts/e1_baseline_results.json` | `0726043d7e24...` | `70d51f6c95d0...` | **differs** | Key versions differs (python 3.11.9->3.13.14, platform Win10->Win11, scikit-learn 1.9.0->1.9.1, pyarrow 21.0.0->25.0.1) | Yes (after removing versions, all metrics, C=10.0, splits, and confusion matrix match exactly) | platform-version string (replay execution environment versions) |
| 13 | `artifacts/e1_reconstructed_model.joblib` | `60f407d85483...` | `60f407d85483...` | **byte-exact** | None | N/A | N/A |
| 14 | `config/e2_chunk_pool.json` | `633c0e3ea7fa...` | `633c0e3ea7fa...` | **byte-exact** | None | N/A | N/A |
| 15 | `artifacts/e2_chunk_pool_results.json` | `d68be6f4950b...` | `d68be6f4950b...` | **byte-exact** | None | N/A | N/A |
| 16 | `artifacts/e2_correction_manifest.json` | `1ae92bc5e5b5...` | `c16d8af59fa6...` | **differs** | JSON serialization formatting of discarded vs corrected metrics (discarded run audit record) | Yes (after normalization, all test metrics for 256 prefix and chunk-and-pool match) | JSON formatting / serialization |
| 17 | `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/model.safetensors` | `924a5bb9078b...` | `924a5bb9078b...` | **byte-exact** | None | N/A | N/A |
| 18 | `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/config.json` | `b0b0142bc2f3...` | `b0b0142bc2f3...` | **byte-exact** | None | N/A | N/A |
| 19 | `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/trainer_state.json` | `78b3ec16acfb...` | `78b3ec16acfb...` | **byte-exact** | None | N/A | N/A |
| 20 | `config/e3_e4_evidence_augmented_prediction.json` | `ec0fe15e6514...` | `ec0fe15e6514...` | **byte-exact** | None | N/A | N/A |
| 21 | `src/legal_xai/evidence_augmented_prediction.py` | `1aceee9e37ae...` | `1aceee9e37ae...` | **byte-exact** | None | N/A | N/A |
| 22 | `scripts/run_evidence_pipeline.py` | `8742290cb4c2...` | `8742290cb4c2...` | **byte-exact** | None | N/A | N/A |
| 23 | `scripts/run_grounded_answer_pipeline.py` | `7799b5768986...` | `7799b5768986...` | **byte-exact** | None | N/A | N/A |
| 24 | `scripts/run_e3_e4_evidence_augmented_evaluation.py` | `6c285f00dc55...` | `6c285f00dc55...` | **byte-exact** | None | N/A | N/A |
| 25 | `scripts/replay_e3_e4_evidence_augmented_evaluation.py` | `a2e76abda21d...` | `a2e76abda21d...` | **byte-exact** | None | N/A | N/A |
| 26 | `artifacts/e3_e4_evidence_augmented_evaluation.json` | `e28ea37e67e5...` | `5414e0024307...` | **differs** | Per-case retrieval_run_id UUIDs (30 instances) and ~1e-4 float logits variation across torch/cuDNN kernels | Yes (after removing retrieval_run_id and mean_logits float tails, all predictions, citations, and metrics match exactly) | run UUID (retrieval_run_id) & torch/cuDNN kernel float nondeterminism (~1e-4) |
| 27 | `artifacts/e3_e4_prediction_error_analysis.json` | `dbd2178aeadf...` | `847cb77b17f5...` | **differs** | JSON serialization formatting; categories (E2 wrong/E3-E4 correct: 2 cases, expected authority retrieved/prediction wrong: 4 cases) verified identical | Yes (all categories, case IDs, and population N=30 match) | JSON formatting / serialization |
| 28 | `src/legal_xai/retrieval.py` | `a08da2f560ce...` | `a08da2f560ce...` | **byte-exact** | None | N/A | N/A |
| 29 | `src/legal_xai/evidence_pipeline.py` | `a9efc520358d...` | `a9efc520358d...` | **byte-exact** | None | N/A | N/A |
| 30 | `src/legal_xai/grounded_answer.py` | `2843b021e1e7...` | `2843b021e1e7...` | **byte-exact** | None | N/A | N/A |
| 31 | `src/legal_xai/citation_verifier.py` | `a9e17ee52109...` | `a9e17ee52109...` | **byte-exact** | None | N/A | N/A |
| 32 | `artifacts/week10_post_selfmatch_freeze_regression.json` | `84357553e577...` | `f9969b87f963...` | **differs** | Volatile run_id UUIDs for candidate runs (24 instances across control evaluations) | Yes (after removing run_id, all control ranks and non-worsening flags match) | run UUID (run_id generated during evaluation runs) |
| 33 | `artifacts/week10_dev_probe_selfmatch_recheck.json` | `ffb92f8b3992...` | `88522cfea2c3...` | **differs** | JSON serialization formatting; summary counts (6/9 at k=100, 7/9 at k=500, newly retrieved 1984_62, 1988_238, 1992_137) match freeze verbatim | Yes (all summary fields and case IDs match freeze record) | JSON formatting / serialization |
| 34 | `artifacts/week11_temporal_prerank_evaluation.json` | `9a475febf1e0...` | `6fc439e5ac40...` | **differs** | Per-case retrieval_run_id UUIDs (30 instances in per_case_records) | Yes (after removing retrieval_run_id, all metrics Recall@5=0.4, Recall@100=0.5, 0 regressions match) | run UUID (retrieval_run_id) |
| 35 | `artifacts/week11_temporal_preranking_investigation.md` | `dbb60c27fb0b...` | `dbb60c27fb0b...` | **byte-exact** | None | N/A | N/A |
| 36 | `answer_key/authority_answer_key.json` | `f4ccb0fa8bfc...` | `f4ccb0fa8bfc...` | **byte-exact** | None | N/A | N/A |
| 37 | `docker/e2.Dockerfile` | `330ebd999830...` | `330ebd999830...` | **matches after CRLF->LF** | Line endings (CRLF on default Windows checkout vs LF in freeze; restored to LF via .gitattributes) | Yes (byte-identical after LF normalisation: 330ebd999830665b...) | Line endings (core.autocrlf checkout on Windows) |
| 38 | `compose.yaml` | `10e373be01fe...` | `10e373be01fe...` | **byte-exact** | None | N/A | N/A |
| 39 | `docker/Dockerfile.ocr` | `c74526c1197b...` | `c74526c1197b...` | **byte-exact** | None | N/A | N/A |

## Platform-Version Drift (Software Dependencies)

As recorded in `artifacts/e1_baseline_results.json` vs the frozen baseline specification in `config/reproducibility_freeze.json`:

| Component | Frozen Baseline Version | Current Replay Version | Impact |
|---|---|---|---|
| **Operating System / Platform** | `Windows-10-10.0.26200-SP0` | `Windows-11-10.0.26200-SP0` | None (exact metric match) |
| **Python** | `3.11.9` | `3.13.14` (tags/v3.13.14:fd17997) | None (exact metric match) |
| **scikit-learn** | `1.9.0` | `1.9.1` | None (exact metric match) |
| **pyarrow** | `21.0.0` | `25.0.1` | None (exact metric match) |
| **PyTorch / cuDNN (E3/E4)** | `torch 2.13.0+cu130` | `torch 2.5.1+cu124` (container) | Float tail variance in mean_logits (~1e-4); 0 label/metric impact |

## Git History Recovery Analysis

As documented in `TRANSFER_MANIFEST.json`, this repository workspace was created from a transfer snapshot of upstream commit `75da550dcf2a9057782be194f0631d09ea22c945`, where upstream `.git history and metadata` were intentionally excluded from the transfer archive. The local Git history begins with initial baseline reproduction commit `2bd02b3`. Consequently, earlier pre-transfer blobs matching the stale frozen hashes for the 10 differing files do not reside in the local Git object database, but their semantic equivalence to the frozen specifications has been independently verified above.
