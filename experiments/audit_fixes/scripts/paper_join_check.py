"""Verify join-derived paper claims from frozen artifacts (read-only)."""
import json
from pathlib import Path

R = Path("/repo")

# 1. Error overlap E1 vs E2 on 1503
e1 = json.load(open(R / "artifacts/e1_test_predictions.json"))
e2 = json.load(open(R / "artifacts/e2_test_predictions.json"))
e1r = {r["case_id"]: (r["true_label"], r.get("E1_mean_logits_prediction", r.get("prediction"))) for r in e1["records"]}
e2r = {r["case_id"]: (r["true_label"], r["E2_mean_logits_prediction"]) for r in e2["records"]}
common = sorted(set(e1r) & set(e2r))
both = e1o = e2o = neither = 0
for c in common:
    t, p1 = e1r[c]
    _, p2 = e2r[c]
    c1, c2 = (p1 == t), (p2 == t)
    both += c1 and c2
    e1o += c1 and not c2
    e2o += (not c1) and c2
    neither += (not c1) and (not c2)
print(f"overlap n={len(common)} both={both} e1only={e1o} e2only={e2o} neither={neither}")

# 2. E2-wrong but E3/E4-correct; recovery-but-wrong-prediction
e34 = json.load(open(R / "artifacts/e3_e4_evidence_augmented_evaluation.json"))
for r in e34["per_case_records"]:
    c = r["query_case_id"]
    e2p = e2r[c][1]
    e3p = r["E3"]["outcome_prediction"]["predicted_label"]
    t = r["true_label"]
    if e2p != t and e3p == t:
        print("E2wrong-E3correct:", c)
    if r["expected_authority_selected"] and e3p != t:
        print("recovered-but-wrong:", c)

# 3. Bucket ranks for retrieved-not-selected
for r in e34["per_case_records"]:
    if r["expected_authority_retrieved_at_100"] and not r["expected_authority_selected"]:
        print("retnotsel:", r["query_case_id"])

# 4. Alignment audit summary
aa = json.load(open(R / "artifacts/answer_key_alignment_audit_corrected.json"))
s = aa.get("summary", {})
print("align summary:", json.dumps(s)[:500])
print("align rows:", len(aa.get("rows", [])))
