#!/bin/bash
set -e
pip install -q "psycopg[binary]==3.3.4" pydantic sqlmodel pyarrow 2>&1 | tail -2
cd /repo
export PYTHONPATH=/repo/src:/repo/scripts

echo "=== BM25 REBUILD ==="
python scripts/build_bm25_index.py \
  --database-url "$LEGAL_XAI_DATABASE_URL" \
  --index /out/bm25.sqlite \
  --output /out/bm25_rebuilt.json

echo "=== MANIFEST COMPARISON ==="
python -c "
import json
frozen  = json.load(open('artifacts/bm25_index.json'))
rebuilt = json.load(open('/out/bm25_rebuilt.json'))
for k in ['chunks_indexed', 'index_version', 'engine', 'tokenizer']:
    m = 'MATCH' if frozen[k] == rebuilt[k] else 'MISMATCH'
    print(f'{k}: frozen={frozen[k]!r} rebuilt={rebuilt[k]!r} -> {m}')
size_match = 'note: SQLite internal pages may differ' if frozen['index_bytes'] != rebuilt['index_bytes'] else 'MATCH'
print(f\"index_bytes: frozen={frozen['index_bytes']} rebuilt={rebuilt['index_bytes']} -> {size_match}\")
"

echo "=== RANKING PROBE ==="
python /repo/experiments/audit_fixes/scripts/bm25_ranking_probe.py \
  --frozen-db  retrieval/bm25.sqlite \
  --rebuilt-db /out/bm25.sqlite \
  --answer-key answer_key/authority_answer_key.json \
  --output     /out/bm25_ranking_probe.json
