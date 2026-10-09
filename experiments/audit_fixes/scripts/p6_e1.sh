#!/bin/bash
pip install -q scikit-learn==1.9.0 pyarrow==21.0.0
cd /repo
export PYTHONPATH=/repo/src
python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model1.joblib --predictions-output /out/e1_test1.json
python scripts/reconstruct_e1_predictions.py --model-output /out/e1_model2.joblib --predictions-output /out/e1_test2.json
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
