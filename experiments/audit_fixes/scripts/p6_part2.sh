#!/bin/bash
echo "--- 5. CORPUS IDENTITY ---"
python scripts/build_ecourts_corpus_identity.py --cleaned-root corpus/ecourts/cleaned --output /out/ecourts_corpus_identity.json || true
python -c '
import json
try:
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
except Exception as e:
    print("Corpus Identity error:", e)
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
        u = str(d["per_case_records"][0].get("retrieval_run_id", "-")) + "..."
    v = d.get("versions", d.get("identity_version", d.get("evaluation_version", d.get("artifact_version", "-"))))
    if isinstance(v, dict): v = "dict(...)"
    print(f"{f} | {sz} | {mt} | {b} | {t} | {u} | {v}")
'

echo "--- 7. PAPER-METRIC SOURCE TRACE ---"
grep -n -C 2 "accuracy_score" /repo/scripts/train_e1_baseline.py || true
grep -n -C 2 "f1_score" /repo/scripts/train_e1_baseline.py || true
grep -n -C 2 "confusion_matrix" /repo/scripts/train_e1_baseline.py || true
echo "Recomputation Check:"
grep -n -C 3 "classifier.predict(" /repo/scripts/reconstruct_e1_predictions.py || true

echo "--- 8. E1 REPLAY CLOSURE ---"
pip install -q scikit-learn==1.9.0 pyarrow==21.0.0
export PYTHONPATH=/repo/src
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model1.joblib --predictions-output /out/e1_test1.json 2>&1 | tee /out/e1_1.log
/usr/bin/time -v python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model2.joblib --predictions-output /out/e1_test2.json 2>&1 | tee /out/e1_2.log

python -c '
import hashlib, json
h1 = hashlib.sha256(open("/out/e1_test1.json", "rb").read()).hexdigest()
h2 = hashlib.sha256(open("/out/e1_test2.json", "rb").read()).hexdigest()
m1 = json.load(open("/out/e1_test1.json"))["reproduced_metrics"]
m2 = json.load(open("/out/e1_test2.json"))["reproduced_metrics"]
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
nproc || true
free -m || true
