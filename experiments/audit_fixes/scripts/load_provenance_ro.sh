#!/bin/bash
set -e
pip install -q "psycopg[binary]==3.3.4" pydantic sqlmodel pyarrow 2>&1 | tail -2
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts
echo "--- LOADING PROVENANCE ---"
python scripts/load_provenance.py \
  --corpus-root corpus \
  --database-url "$LEGAL_XAI_DATABASE_URL" \
  --output /out/provenance_load.json
cat /out/provenance_load.json
