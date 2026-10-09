#!/bin/bash
set -e
exec 2>&1

echo "--- 3. 1503 VS 1517 ---"
cat /repo/src/legal_xai/facts.py | grep -A 10 "def facts_input_is_eligible"

pip install -q pandas pyarrow
export PYTHONPATH=/repo/src
python -c '
import json
from pathlib import Path
from legal_xai.facts import load_facts_extraction_rule, extract_case_facts, facts_input_is_eligible
import pyarrow.parquet as pq

rule = load_facts_extraction_rule("/repo/config/facts_extraction.json")
ak = json.load(open("/repo/answer_key/authority_answer_key.json"))
ak_ids = [e["query_case_id"] for e in ak["entries"]]
print(f"answer-key population size: {len(ak_ids)}")

df = pq.read_table("/repo/corpus/ildc/single_test.parquet").to_pandas()
print(f"E1 evaluation population (full test set) size before filter: {len(df)}")

excluded = []
for _, row in df.iterrows():
    text = row.get("text", "")
    res = extract_case_facts(text, rule)
    if not facts_input_is_eligible(res, rule):
        if res.source_char_count == 0:
            reason = "empty_input"
        elif res.retained_char_count / res.source_char_count < rule.minimum_retained_fraction:
            reason = f"retained_fraction={res.retained_char_count/res.source_char_count:.2f} < {rule.minimum_retained_fraction}"
        else:
            reason = f"word_count={len(res.text.split())} < {rule.minimum_facts_words}"
        excluded.append((row["id"], reason))

print(f"Excluded count: {len(excluded)}")
for eid, reason in excluded:
    in_ak = eid in ak_ids
    print(f"ID: {eid}, Reason: {reason}, In answer key: {in_ak}")
'

echo "--- 4. BM25 REBUILD ---"
pip install -q psycopg[binary] sqlmodel pydantic pyarrow

cd /repo
export PYTHONPATH=/repo/src
python scripts/build_bm25_index.py --cleaned-root corpus/ecourts/cleaned --output /out/bm25.sqlite --manifest /out/bm25_index.json || true

python -c '
import json
import sqlite3
import hashlib
import os

def get_db_hash(path):
    if not os.path.exists(path): return "MISSING"
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

print("Rebuilt SQLite hash:", get_db_hash("/out/bm25.sqlite"))
print("Frozen SQLite hash:", get_db_hash("/repo/retrieval/bm25.sqlite"))

if get_db_hash("/out/bm25.sqlite") == get_db_hash("/repo/retrieval/bm25.sqlite"):
    print("BM25 SQLite: IDENTICAL")
else:
    print("BM25 SQLite: DIFFERS")
    print("INSPECTING DIFFERENCES...")
    # Basic inspection
    db1 = sqlite3.connect("/repo/retrieval/bm25.sqlite")
    db2 = sqlite3.connect("/out/bm25.sqlite")
    c1 = db1.execute("SELECT count(*) FROM chunk_doc").fetchone()[0]
    c2 = db2.execute("SELECT count(*) FROM chunk_doc").fetchone()[0]
    print(f"Doc count: Frozen={c1}, Rebuilt={c2}")

d1 = json.load(open("/repo/artifacts/bm25_index.json"))
d2 = json.load(open("/out/bm25_index.json"))
ignore = ["built_at_utc"]
for k in ignore:
    d1.pop(k, None)
    d2.pop(k, None)
s1 = json.dumps(d1, sort_keys=True)
s2 = json.dumps(d2, sort_keys=True)
print(f"Removed volatile keys before comparison: {ignore}")
if s1 == s2:
    print("BM25 manifest: IDENTICAL")
else:
    print("BM25 manifest: DIFFERS")
'

echo "--- 5. CORPUS IDENTITY ---"
python scripts/build_ecourts_corpus_identity.py --cleaned-root corpus/ecourts/cleaned --output /out/ecourts_corpus_identity.json
python -c '
import json
d1 = json.load(open("/repo/artifacts/ecourts_corpus_identity.json"))
d2 = json.load(open("/out/ecourts_corpus_identity.json"))
ignore = ["timestamp", "identity_version", "evaluation_version", "versions"]
for k in ignore:
    d1.pop(k, None)
    d2.pop(k, None)
s1 = json.dumps(d1, sort_keys=True)
s2 = json.dumps(d2, sort_keys=True)
print(f"Removed keys: {ignore}")
if s1 == s2: print("Corpus Identity: IDENTICAL")
else: print("Corpus Identity: DIFFERS")
'

echo "--- 6. DRIFTED FILES ---"
python -c '
import os, json, time
files = [
    "artifacts/bm25_index.json",
    "artifacts/e1_baseline_results.json",
    "artifacts/e2_correction_manifest.json",
    "artifacts/e3_e4_evidence_augmented_evaluation.json",
    "artifacts/e3_e4_prediction_error_analysis.json",
    "artifacts/week10_post_selfmatch_freeze_regression.json",
    "artifacts/week10_dev_probe_selfmatch_recheck.json",
    "artifacts/week11_temporal_prerank_evaluation.json",
    "artifacts/ecourts_corpus_identity.json"
]
print("path | size | mtime | built_at | timestamp | uuid/run_id | version fields")
for f in files:
    full = "/repo/" + f
    sz = os.path.getsize(full)
    mt = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getmtime(full)))
    d = json.load(open(full))
    b = d.get("built_at_utc", d.get("built_at", "-"))
    t = d.get("timestamp", "-")
    u = d.get("run_id", d.get("retrieval_run_id", "-"))
    if u == "-" and "per_case_records" in d and len(d["per_case_records"]) > 0:
        u = d["per_case_records"][0].get("retrieval_run_id", "-") + "..."
    v = d.get("versions", d.get("identity_version", d.get("evaluation_version", d.get("artifact_version", "-"))))
    print(f"{f} | {sz} | {mt} | {b} | {t} | {u} | {v}")
'

echo "--- 7. PAPER-METRIC SOURCE TRACE ---"
grep -n -C 5 "accuracy_score" /repo/scripts/reconstruct_e1_predictions.py || true
grep -n -C 5 "f1_score" /repo/scripts/reconstruct_e1_predictions.py || true
grep -n -C 5 "confusion_matrix" /repo/scripts/reconstruct_e1_predictions.py || true
echo "Recomputation Check:"
grep -n -C 5 "clf.predict" /repo/scripts/reconstruct_e1_predictions.py || true

echo "--- 8. E1 REPLAY CLOSURE ---"
pip install -q scikit-learn==1.9.0
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model1.joblib --predictions-output /out/e1_test1.json 2>&1 | tee /out/e1_1.log
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model2.joblib --predictions-output /out/e1_test2.json 2>&1 | tee /out/e1_2.log

python -c '
import hashlib, json
h1 = hashlib.sha256(open("/out/e1_test1.json", "rb").read()).hexdigest()
h2 = hashlib.sha256(open("/out/e1_test2.json", "rb").read()).hexdigest()
m1 = json.load(open("/out/e1_test1.json"))["test_metrics"]
m2 = json.load(open("/out/e1_test2.json"))["test_metrics"]
print(f"Run 1 hash: {h1}")
print(f"Run 2 hash: {h2}")
if h1 == h2 and m1 == m2:
    print("E1 repeated replay: IDENTICAL")
elif m1 == m2:
    print("E1 repeated replay: NUMERICALLY_EQUIVALENT")
else:
    print("E1 repeated replay: NON-DETERMINISTIC")
'

echo "--- 9. MACHINE INFO ---"
nproc
free -m
docker info | grep Memory || true
nvidia-smi || true
