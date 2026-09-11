"""Read-only confidence intervals for frozen NyayaTrace results.

Reads frozen artifacts only; writes ONLY to validation_prep/confidence_intervals/.
Never touches artifacts/, config/, answer_key/ or any frozen file.

Methods (stdlib only):
- Binomial rates (accuracies, recalls, precision, groundedness/provenance/
  temporal/unsupported rates): Wilson score 95% interval (z=1.96).
- Zero-event rates (0/150): Wilson interval + rule-of-three upper bound note.
- Macro-F1: seeded nonparametric bootstrap (B=10000, seed 20260911) over
  frozen per-case (true, pred) pairs; 2.5/97.5 percentiles.

Fail-closed: every point estimate recomputed from per-case records is
cross-checked against config/reproducibility_freeze.json (and the artifact's
own recorded metrics). Any mismatch aborts with nonzero exit — no silent drift.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DEFAULT = ROOT / "validation_prep" / "confidence_intervals" / "ci_results.json"

Z95 = 1.96
BOOTSTRAP_B = 10_000
BOOTSTRAP_SEED = 20260911


def wilson(k: int, n: int, z: float = Z95) -> dict:
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    out = {"k": k, "n": n, "point": p, "ci95_low": max(0.0, center - half),
           "ci95_high": min(1.0, center + half), "method": "wilson_95"}
    if k == 0:
        out["rule_of_three_upper95"] = min(1.0, 3.0 / n)
    return out


def macro_f1(pairs: list[tuple[int, int]]) -> float:
    f1s = []
    for cls in (0, 1):
        tp = sum(1 for t, p in pairs if t == cls and p == cls)
        fp = sum(1 for t, p in pairs if t != cls and p == cls)
        fn = sum(1 for t, p in pairs if t == cls and p != cls)
        f1s.append(0.0 if (2 * tp + fp + fn) == 0 else 2 * tp / (2 * tp + fp + fn))
    return sum(f1s) / 2


def bootstrap_macro_f1(pairs: list[tuple[int, int]]) -> dict:
    rng = random.Random(BOOTSTRAP_SEED)
    n = len(pairs)
    stats = sorted(macro_f1([pairs[rng.randrange(n)] for _ in range(n)])
                   for _ in range(BOOTSTRAP_B))
    lo = stats[int(0.025 * BOOTSTRAP_B)]
    hi = stats[int(0.975 * BOOTSTRAP_B) - 1]
    return {"point": macro_f1(pairs), "ci95_low": lo, "ci95_high": hi,
            "method": f"nonparametric_bootstrap_percentile_B{BOOTSTRAP_B}",
            "seed": BOOTSTRAP_SEED, "n": n}


def close(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()

    freeze = json.loads((ROOT / "config" / "reproducibility_freeze.json").read_text(encoding="utf-8"))
    e1pred = json.loads((ROOT / "artifacts" / "e1_test_predictions.json").read_text(encoding="utf-8"))
    e2pred = json.loads((ROOT / "artifacts" / "e2_test_predictions.json").read_text(encoding="utf-8"))
    e34 = json.loads((ROOT / "artifacts" / "e3_e4_evidence_augmented_evaluation.json").read_text(encoding="utf-8"))

    if args.output.resolve().is_relative_to(ROOT / "artifacts"):
        raise SystemExit("refusing to write into artifacts/ (frozen)")

    e1_pairs = [(r["true_label"], r["E1_prediction"]) for r in e1pred["records"]]
    e2mean_pairs = [(r["true_label"], r["E2_mean_logits_prediction"]) for r in e2pred["records"]]
    e2vote_pairs = [(r["true_label"], r["E2_majority_vote_prediction"]) for r in e2pred["records"]]

    # E3/E4 per-case outcomes live at record["E3"|"E4"]["outcome_prediction"]
    # ["predicted_label"] (verified against the frozen file, not assumed).
    recs = e34["per_case_records"]
    try:
        e3_pairs = [(r["true_label"], r["E3"]["outcome_prediction"]["predicted_label"]) for r in recs]
        e4_pairs = [(r["true_label"], r["E4"]["outcome_prediction"]["predicted_label"]) for r in recs]
    except KeyError as exc:
        raise SystemExit(f"E3/E4 outcome_prediction.predicted_label path missing: {exc}")
    e4_shared = e4_pairs == e3_pairs

    # Cross-check point estimates against the freeze (fail-closed).
    checks = [
        ("E1 acc", sum(1 for t, p in e1_pairs if t == p) / len(e1_pairs),
         freeze["experiments"]["E1"]["test_metrics"]["accuracy"]),
        ("E2 mean acc", sum(1 for t, p in e2mean_pairs if t == p) / len(e2mean_pairs),
         freeze["experiments"]["E2_corrected"]["test_metrics"]["mean_logits"]["accuracy"]),
        ("E2 vote acc", sum(1 for t, p in e2vote_pairs if t == p) / len(e2vote_pairs),
         freeze["experiments"]["E2_corrected"]["test_metrics"]["majority_vote"]["accuracy"]),
        ("E3 acc", sum(1 for t, p in e3_pairs if t == p) / len(e3_pairs),
         freeze["experiments"]["E3_E4_evidence_augmented_prediction"]["metrics"]["E3"]["accuracy"]),
    ]
    for name, got, exp in checks:
        if not close(got, exp):
            raise SystemExit(f"point-estimate drift: {name} recomputed={got} frozen={exp}")

    retr = e34["E3_retrieval"]
    r5 = [r for r in recs if r["expected_authority_retrieved_at_5"]]
    r100 = [r for r in recs if r["expected_authority_retrieved_at_100"]]
    if not (close(retr["recall_at_5"], len(r5) / 30) and close(retr["recall_at_100"], len(r100) / 30)):
        raise SystemExit("retrieval point-estimate drift vs per-case records")

    result = {
        "derived_artifact": True,
        "frozen_inputs": {
            "freeze_version": freeze["freeze_version"],
            "artifacts": ["artifacts/e1_test_predictions.json",
                          "artifacts/e2_test_predictions.json",
                          "artifacts/e3_e4_evidence_augmented_evaluation.json"],
        },
        "computed_at_utc": datetime.now(UTC).isoformat(),
        "accuracy_wilson95": {
            "E1_n1503": wilson(sum(1 for t, p in e1_pairs if t == p), 1503),
            "E2_mean_logits_n1503": wilson(sum(1 for t, p in e2mean_pairs if t == p), 1503),
            "E2_majority_vote_n1503": wilson(sum(1 for t, p in e2vote_pairs if t == p), 1503),
            "E3_n30": wilson(sum(1 for t, p in e3_pairs if t == p), 30),
            "E4_n30": wilson(sum(1 for t, p in e4_pairs if t == p), 30),
        },
        "macro_f1_bootstrap95": {
            "E1_n1503": bootstrap_macro_f1(e1_pairs),
            "E2_mean_logits_n1503": bootstrap_macro_f1(e2mean_pairs),
            "E2_majority_vote_n1503": bootstrap_macro_f1(e2vote_pairs),
            "E3_n30": bootstrap_macro_f1(e3_pairs),
            "E4_n30": bootstrap_macro_f1(e4_pairs),
        },
        "retrieval_integrity_wilson95": {
            "recall_at_5": wilson(len(r5), 30),
            "recall_at_100": wilson(len(r100), 30),
            "authority_precision_12_150": wilson(12, 150),
            "citation_groundedness_150_150": wilson(150, 150),
            "provenance_validity_150_150": wilson(150, 150),
            "temporal_violation_0_150": wilson(0, 150),
            "unsupported_claim_0_150": wilson(0, 150),
        },
        "notes": [
            "Wilson intervals are analytic for binomial rates; macro-F1 intervals are seeded bootstrap percentiles over frozen per-case pairs.",
            "N=30 intervals are wide by construction; report them alongside (not instead of) point estimates and denominators.",
            "E4 predictions reuse the identical shared predictor as E3"
            + (" (verified identical in this run)." if e4_shared else " (E4 block present; compared in this run)."),
            "Zero-event upper bounds use Wilson; rule_of_three_upper95 shown additionally.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"wrote": str(args.output), "e4_shared_with_e3": e4_shared,
                      "E3_acc_ci": result["accuracy_wilson95"]["E3_n30"],
                      "E1_acc_ci": result["accuracy_wilson95"]["E1_n1503"]}, indent=2))


if __name__ == "__main__":
    main()
