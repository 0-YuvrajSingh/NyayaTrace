# Dependency references (read-only grep; 2026-09-29)

## e2_cache (window cache) consumers — ACTIVE runtime
- scripts/prepare_e2_chunk_pool_cache.py:88 (builder; writes train/val/test splits)
- scripts/infer_e2_checkpoint_predictions.py:47-48 (default --cache-dir; reads
  input_ids/attention_mask/token_type_ids/document_indices + metadata.json)
- scripts/timed_e2_repeat.py:10-12 (verified repeat wrapper; --cache-dir /cache/test)
- experiments/audit_fixes/scripts/run_e2_repeat.sh + run_e2_repeat2.sh (verified runs
  mount replay/e2_cache at /cache:ro and /cache/test)
- config/e2_chunk_pool.json + artifacts/e2_chunk_pool_results.json (window counts
  33702/6054/9576 referenced as frozen record)
- scripts/build_reproducibility_freeze.py:128-130,159 (freeze references to cache paths)
- Historical: scripts/train_e2_chunk_pool_cached.py:46,49 (training-time cache use)

## HF cache consumers — ACTIVE runtime
- All E2/E3 GPU runs mount an HF cache at HF_HOME/HF_HUB_OFFLINE=1:
  frozen artifacts/e2_hf_cache (mounted :ro) or writable replay/e2_hf_cache copy.
- Tokenizer + model blobs for law-ai/InLegalBERT revision b5ecfed8…

## validation_replay/ consumers — NONE FOUND in active code
- No script, config, Dockerfile, compose, test, doc, or paper file references
  `validation_replay/` (grep over scripts/, src/, config/, compose*, demo/, docs/,
  experiments/audit_fixes/scripts/, paper tex: zero hits).
- Self-contained prior replay: own manifests (asset_inventory.json,
  baseline_execution_metadata.json, freeze_validation.json, metric_comparison.json).
- Runtime discovery risk: LOW (path never constructed dynamically in code; only
  literal references exist and none point there).

## Distinction
Active runtime dependencies: replay/e2_cache + one HF cache.
Historical/audit references only: validation_replay/ tree, early runner scripts.
