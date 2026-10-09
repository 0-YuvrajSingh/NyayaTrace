#!/bin/bash
set -e
pip install -q "psycopg[binary]==3.3.4" pyarrow==21.0.0 scikit-learn==1.9.0 rank-bm25==0.2.2 2>&1 | tail -2
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts
echo "=== E3/E4 REPLAY ==="
python scripts/replay_e3_e4_evidence_augmented_evaluation.py \
  --reference artifacts/e3_e4_evidence_augmented_evaluation.json 2>&1
