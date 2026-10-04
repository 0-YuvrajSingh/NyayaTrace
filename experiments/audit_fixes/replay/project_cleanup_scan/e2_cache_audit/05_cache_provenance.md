# Cache provenance (read-only)

## replay/e2_cache/ — VERIFIED-RUN cache (2026-09-28)
Created by the audited E2 preparation (e2_cache_prep.log: 5020/33702, 983/6054,
1503/9576, matching frozen record). Consumed read-only by both exact-reproduction
inference runs (e2_inference.log, e2_repeat2.log: wall 89.5s, records identical).
This is the cache of record for the verified E2 result.

## validation_replay/e2_cache/ — PRIOR independent replay (2026-09-11 era)
Per validation_replay/baseline_execution_metadata.json: a separate "REAL BASELINE
REPRODUCTION" against a transfer copy of the repo (different machine path
C:/Users/uvi58/... — same user, earlier environment; record 2026-09-11, "no git
history/transfer copy"). 19/19 files byte-identical to the verified-run cache
(deterministic builder output), with older mtimes. Self-contained with own
reproduced predictions (e2/e2_reproduced_predictions.json, 213,928B — same size as
frozen; hash comparison left to a later phase if needed). Classification: historical
independent-replay artifact, NOT the verified-run cache, NOT referenced by active code.

## artifacts/e2_hf_cache/ — FROZEN hub cache
Original pinned model/tokenizer blobs (revision b5ecfed8…). Read-only mount source.

## replay/e2_hf_cache/ — WRITABLE working copy (2026-09-28)
Copied (xcopy) from frozen to give Docker a writable HF_HOME. Blobs identical (6/6);
3 extra materialized snapshot files (vocab.txt, tokenizer_config.json,
special_tokens_map) + runtime locks. Derived, regenerable by re-copy + re-run.
