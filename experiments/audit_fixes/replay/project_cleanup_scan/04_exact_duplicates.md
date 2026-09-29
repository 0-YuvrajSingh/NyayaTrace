# Exact duplicates (5,320 groups; full data in _dup_groups.json)

Provenance: SHA-256 over full bytes (42,469 files). Reference checks below are
filename/text searches, not deletions.

## Major groups (by size)
| SHA (prefix) | size | paths |
| --- | --- | --- |
| 4c5b13… | 534,276,705 | artifacts/e2_hf_cache/.../blobs/4c5b13…zip = experiments/audit_fixes/replay/e2_hf_cache/.../same |
| 293b54… | 534,217,728 | artifacts/e2_hf_cache/.../blobs/293b54… = replay/e2_hf_cache/.../same |
| e2_cache train input_ids | 69,021,824 | replay/e2_cache/train/input_ids.npy = validation_replay/e2_cache/train/input_ids.npy |
| spring jar | 21,332,556 | demo/spring-api/target/*.jar = replay/spring-api-copy/target/*.jar |
| e2_cache test input_ids | 19,611,776 | replay/e2_cache/test/input_ids.npy = validation_replay/e2_cache/test/input_ids.npy |

## Pattern groups
- **corpus/ecourts PDFs (5,182 groups)**: same PDF bytes stored under two `year=` directories
  (e.g. `year=1981/1982_2_365_1455_EN.pdf` = `year=1982/1982_2_365_1455_EN.pdf`).
  File-level manifestation of the SCR-volume-year vs decision-date skew. Tracked? No
  (ignored corpus data). Referenced by code? Chunks (not raw PDFs) are indexed; dedup
  crosswalk governs identity. Timestamps/names differ by design (year folders).
  Recommendation class: REVIEW_REQUIRED (corpus layout decision, not audit-level deletion).
- **HF hub cache (8 groups + locks)**: `artifacts/e2_hf_cache` = `replay/e2_hf_cache`
  (intentional writable copy made 2026-09-28 for Docker). ~1GB duplicated. Neither tracked.
  Referenced by: E2/E3 replay scripts via HF_HOME. Recommendation: DUPLICATE_CANDIDATE (keep until replays done).
- **e2_cache (replay = validation_replay)**: identical window caches incl. 69MB + 19MB
  input_ids.npy. validation_replay/ purpose unclear (older replay attempt?). Neither tracked.
  Recommendation: DUPLICATE_CANDIDATE, needs owner decision on validation_replay/ role.
- **spring-api jar + target/**: `demo/spring-api/target` = `replay/spring-api-copy/target`
  (copied tree for audit). Maven `target/` is regenerable (`mvn package`).
  Recommendation: GENERATED_REGENERABLE (copy side deletable later).
- **figures**: `figures/*.pdf` = `artifacts/figures/*.pdf` (fig1-5; exact dups).
  `figures/` is referenced by paper tex (`\includegraphics{figures/...}`); `artifacts/figures/`
  is the frozen copy. Recommendation: DUPLICATE_CANDIDATE (keep `figures/`, archive other).
- **artifacts/e2_test_predictions.json = replay/e2_test_predictions.json** (exact replay match,
  expected — evidence, KEEP both sides as cross-validation).
- **artifacts/ecourts_corpus_identity.json = replay/ecourts_corpus_identity.json** (same pattern).
- **replay e1_test1.json = e1_test2.json?** No — hashes differ (1F4CD… vs 0218E6…); near-dups, see 05.
- **demo/web + demo/spring-api (43 + 35 groups)**: node_modules / Maven cache duplicates
  (identical dependency files). Ignored build artifacts. Recommendation: GENERATED_REGENERABLE.
- **audit scripts (42 groups in experiments/audit_fixes)**: repeated small helper/logs?
  Detail in 07; mostly distinct files sharing boilerplate hashes unlikely at SHA-256 —
  these are likely small identical files (e.g. 101-byte e1_1.log/e1_2.log). Verify per-group before action.

Per-group tracked/referenced/timestamp detail: see _dup_groups.json + 01_full_inventory.csv.
No deletion performed or decided here.
