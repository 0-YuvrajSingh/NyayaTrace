"""Diagnose E3/E4 stable-hash mismatch without GPU: inspect frozen artifact ordering and keys."""
import json
from pathlib import Path

ROOT = Path("/repo")
ref = json.loads((ROOT / "artifacts/e3_e4_evidence_augmented_evaluation.json").read_text())
ak = json.loads((ROOT / "answer_key/authority_answer_key.json").read_text())

ak_order = [str(e["query_case_id"]) for e in ak["entries"] if e.get("status") == "evaluation"]
ref_order = [str(r["query_case_id"]) for r in ref["per_case_records"]]
print("answer_key eval order == ref per_case order:", ak_order == ref_order)
print("ak_order:", ak_order)
print("ref_order:", ref_order)

r0 = ref["per_case_records"][0]
print("per-case keys:", sorted(r0.keys()))
print("E3 keys:", sorted(r0["E3"].keys()))
print("E4 keys:", sorted(r0["E4"].keys()))
se0 = r0["E3"]["selected_evidence"][0]
print("selected_evidence[0] keys:", sorted(se0.keys()))
print("bm25_score type/value:", type(se0.get("bm25_score")).__name__, repr(se0.get("bm25_score")))
print("rank type/value:", type(se0.get("rank")).__name__, repr(se0.get("rank")))
print("E3 prediction:", r0["E3"]["outcome_prediction"])
print("top-level keys:", sorted(ref.keys()))
print("prediction_config model checkpoint:", ref["prediction_config"]["model"]["checkpoint"])
# Check for any UUID-like or timestamp-like values in frozen (nondeterministic candidates)
import re
uuid_re = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)
s = json.dumps(ref)
uuids = set(uuid_re.findall(s))
print("uuid-like values in frozen (should be only retrieval_run_ids):", len(uuids))
# keys named run_id (not retrieval_run_id) that comparator does NOT exclude
def find_keys(obj, path=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "run_id":
                hits.append(path + "/" + k)
            hits += find_keys(v, path + "/" + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += find_keys(v, f"{path}[{i}]")
    return hits
print("keys exactly named 'run_id' (NOT excluded by comparator):", find_keys(ref)[:10])
