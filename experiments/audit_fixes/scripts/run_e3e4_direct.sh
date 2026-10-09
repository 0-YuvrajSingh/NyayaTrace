#!/bin/bash
set -e
pip install -q "psycopg[binary]==3.3.4" pyarrow==21.0.0 scikit-learn==1.9.0 rank-bm25==0.2.2 2>&1 | tail -1
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts
echo "=== E3/E4 DIRECT REPLAY TO PERSISTENT OUTPUT ==="
python scripts/run_e3_e4_evidence_augmented_evaluation.py \
  --output /out/e3e4_replay.json --force 2>&1
