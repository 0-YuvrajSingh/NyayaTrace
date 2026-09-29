"""Verify E3/E4 functional equivalence: labels + evidence IDs for all 30."""
import json
from pathlib import Path

ref = json.loads(Path("/repo/artifacts/e3_e4_evidence_augmented_evaluation.json").read_text())
rep = json.loads(Path("/out/e3e4_replay.json").read_text())
rr = {r["query_case_id"]: r for r in ref["per_case_records"]}
pr = {r["query_case_id"]: r for r in rep["per_case_records"]}

label_match = sum(1 for c in rr if rr[c]["E3"]["outcome_prediction"]["predicted_label"] == pr[c]["E3"]["outcome_prediction"]["predicted_label"])
e4_match = sum(1 for c in rr if rr[c]["E4"]["outcome_prediction"]["predicted_label"] == pr[c]["E4"]["outcome_prediction"]["predicted_label"])
ev_match = 0
logit_maxdiff = 0.0
for c in rr:
    a = [e["chunk_id"] for e in rr[c]["E3"]["selected_evidence"]]
    b = [e["chunk_id"] for e in pr[c]["E3"]["selected_evidence"]]
    if a == b:
        ev_match += 1
    else:
        print(f"{c} evidence DIFFERS")
    la = rr[c]["E3"]["outcome_prediction"]["mean_logits"]
    lb = pr[c]["E3"]["outcome_prediction"]["mean_logits"]
    logit_maxdiff = max(logit_maxdiff, abs(la[0]-lb[0]), abs(la[1]-lb[1]))
print(f"E3 labels identical: {label_match}/30")
print(f"E4 labels identical: {e4_match}/30")
print(f"selected evidence chunk_ids identical: {ev_match}/30")
print(f"max abs mean_logit diff: {logit_maxdiff:.8f}")
print("E3==E4 within each run (parity):",
      all(r["E3"]["outcome_prediction"]==r["E4"]["outcome_prediction"] for r in ref["per_case_records"]),
      all(r["E3"]["outcome_prediction"]==r["E4"]["outcome_prediction"] for r in rep["per_case_records"]))
