#!/bin/bash
set -e
pip install -q "psycopg[binary]==3.3.4" pyarrow==21.0.0 scikit-learn==1.5.2 2>&1 | tail -1
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts
python experiments/audit_fixes/scripts/bm25_deep_compare.py \
  --frozen-db retrieval/bm25.sqlite \
  --rebuilt-db /out/bm25.sqlite \
  --answer-key answer_key/authority_answer_key.json \
  --test-split corpus/ildc/single_test.parquet \
  --facts-config config/facts_extraction.json \
  --output /out/bm25_deep_compare.json
