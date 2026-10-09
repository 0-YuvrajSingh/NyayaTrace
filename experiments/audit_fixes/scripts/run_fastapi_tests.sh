#!/bin/bash
set -e
pip install -q fastapi uvicorn "httpx==0.28.1" "psycopg[binary]==3.3.4" scikit-learn==1.9.0 pyarrow==21.0.0 rank-bm25==0.2.2 pytest==9.1.1 2>&1 | tail -2
export PYTHONPATH=/repo/src:/repo/scripts
cd /repo/demo/ml-service
echo "=== FASTAPI TESTS ==="
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -q tests/ 2>&1
