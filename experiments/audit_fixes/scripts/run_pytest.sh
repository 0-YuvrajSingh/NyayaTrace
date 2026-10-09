#!/bin/bash
set -e
pip install -q "psycopg[binary]==3.3.4" pyarrow==21.0.0 scikit-learn==1.9.0 rank-bm25==0.2.2 pytest==9.1.1 2>&1 | tail -2
pip install -q torch==2.5.1+cpu transformers==4.46.3 --index-url https://download.pytorch.org/whl/cpu 2>&1 | tail -2
export PYTHONPATH=/repo/src:/repo/scripts
cd /repo
echo "=== PYTEST ==="
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q tests/ 2>&1
