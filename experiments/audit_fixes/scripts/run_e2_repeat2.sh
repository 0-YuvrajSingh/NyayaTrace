#!/bin/bash
set -e
pip install -q 'psycopg[binary]==3.3.4' pyarrow==21.0.0 scikit-learn==1.5.2 2>&1 | tail -1
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts
echo "=== E2 REPEAT WITH WALL TIME (python resource wrapper) ==="
time -p python scripts/timed_e2_repeat.py 2>&1
