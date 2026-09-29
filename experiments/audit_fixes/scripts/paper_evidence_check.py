"""Batch-check paper quantitative claims against frozen artifacts (read-only)."""
import json
from pathlib import Path

R = Path("/repo")
out = []


def show(label, value):
    out.append(f"{label}: {value}")


# Corpus identity
ident = json.loads((R / "artifacts/ecourts_corpus_identity.json").read_text())
show("identity jsonl_record_count", ident["cleaned_corpus"]["jsonl_record_count"])
show("identity keys", sorted(ident.keys()))

# E1 baseline test metrics
e1 = json.loads((R / "artifacts/e1_baseline_results.json").read_text())
show("e1 keys", sorted(e1.keys()))
for k in ("test_metrics", "test_accuracy", "accuracy", "macro_f1"):
    if k in e1:
        show(f"e1[{k}]", e1[k])

# E2 results test metrics
e2 = json.loads((R / "artifacts/e2_chunk_pool_results.json").read_text())
show("e2 test_document_metrics", e2["test_document_metrics"])
show("e2 splits test eligible/excluded", (e2["splits"]["test"]["eligible_rows"], e2["splits"]["test"]["excluded_rows"]))

# E2 predictions majority vote
e2p = json.loads((R / "artifacts/e2_test_predictions.json").read_text())
show("e2p majority_vote_metrics", e2p["majority_vote_metrics"])

# E3/E4 frozen aggregates
e34 = json.loads((R / "artifacts/e3_e4_evidence_augmented_evaluation.json").read_text())
show("e34 E3_outcome", e34["E3_outcome_prediction"])
show("e34 E3_retrieval", e34["E3_retrieval"])

# Answer key counts
ak = json.loads((R / "answer_key/authority_answer_key.json").read_text())
show("answer_key total entries", len(ak["entries"]))
show("answer_key eval entries", sum(1 for e in ak["entries"] if e.get("status") == "evaluation"))

# Alignment audit corrected
aa = json.loads((R / "artifacts/answer_key_alignment_audit_corrected.json").read_text())
show("align audit keys", sorted(aa.keys())[:20])

# Reproducibility audit week16
w16 = json.loads((R / "artifacts/week16_reproducibility_audit.json").read_text())
show("w16 keys", sorted(w16.keys())[:20])

print("\n".join(out))
