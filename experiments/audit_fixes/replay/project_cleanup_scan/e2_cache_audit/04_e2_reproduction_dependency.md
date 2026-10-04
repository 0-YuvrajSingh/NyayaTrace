# E2 reproduction dependency path (verified audit evidence)

Verified E2 exact reproduction (×2, bit-identical records) used:
1. Window cache: replay/e2_cache (prepared 2026-09-28 via prepare_e2_chunk_pool_cache.py;
   counts 5020/33702, 983/6054, 1503/9576 match frozen record exactly)
   mounted read-only at /cache; inference reads /cache/test.
2. Checkpoint: artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318 (frozen,
   model.safetensors SHA 924a5bb9… verified in-container).
3. Tokenizer/model hub assets: HF cache (frozen artifacts copy :ro, or writable replay
   copy with HF_HUB_OFFLINE=1); all 6 blobs byte-identical between copies.
4. Config: config/e2_chunk_pool.json; seed 202607; batch 8; fp16; RTX 3050.

Regenerability: window cache regenerates deterministically from corpus ILDC parquet +
facts rule + tokenizer (byte-identical outputs proven: validation_replay copy from
2026-09-11 matches ours exactly across 19/19 files). HF blobs re-downloadable from
pinned model id + revision (network + license availability assumed); snapshot extras
(vocab.txt, tokenizer_config.json, special_tokens_map) materialize automatically.
Checkpoint itself is NOT regenerable without retraining (3-epoch GPU run) — frozen,
must be preserved (it is, in artifacts/).

Therefore the required-for-reproduction set is: checkpoint (frozen) + EITHER window
cache copy + EITHER HF blob set + config + scripts. No single cache copy is
irreplaceable except as evidence of the specific verified run.
