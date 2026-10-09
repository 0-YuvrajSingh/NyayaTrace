#!/bin/bash
set -e
pip install -q 'psycopg[binary]==3.3.4' pyarrow==21.0.0 scikit-learn==1.5.2 2>&1 | tail -1
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts
echo "=== E2 REPEAT WITH WALL TIME ==="
/usr/bin/time -v python scripts/infer_e2_checkpoint_predictions.py \
  --cache-dir /cache/test \
  --checkpoint artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318 \
  --recorded-result artifacts/e2_chunk_pool_results.json \
  --output /out/e2_test_predictions_repeat.json \
  --batch-size 8 2>&1
