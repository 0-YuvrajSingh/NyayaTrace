"""Build prediction-aware error analysis from the new E3/E4 evaluation artifact."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    evaluation = json.loads(
        (ROOT / "artifacts/e3_e4_evidence_augmented_evaluation.json").read_text(encoding="utf-8")
    )
    e2 = json.loads((ROOT / "artifacts/e2_test_predictions.json").read_text(encoding="utf-8"))
    e2_by_id = {str(row["case_id"]): row for row in e2["records"]}

    categories: dict[str, list[str]] = {
        "E2_wrong_E3_E4_correct": [],
        "E3_correct_E4_wrong": [],
        "E3_wrong_E4_correct": [],
        "E3_E4_prediction_correct_citation_unsupported": [],
        "expected_authority_retrieved_prediction_wrong": [],
        "citation_traceable_but_expected_authority_not_selected": [],
    }
    for row in evaluation["per_case_records"]:
        case_id = str(row["query_case_id"])
        truth = int(row["true_label"])
        e3_correct = int(row["E3"]["outcome_prediction"]["predicted_label"]) == truth
        e4_correct = int(row["E4"]["outcome_prediction"]["predicted_label"]) == truth
        e2_correct = int(e2_by_id[case_id]["E2_mean_logits_prediction"]) == truth
        citations_supported = row["E4"]["citation_status"]["status"] == "passed"

        if not e2_correct and e3_correct and e4_correct:
            categories["E2_wrong_E3_E4_correct"].append(case_id)
        if e3_correct and not e4_correct:
            categories["E3_correct_E4_wrong"].append(case_id)
        if not e3_correct and e4_correct:
            categories["E3_wrong_E4_correct"].append(case_id)
        if e3_correct and e4_correct and not citations_supported:
            categories["E3_E4_prediction_correct_citation_unsupported"].append(case_id)
        if row["expected_authority_retrieved_at_100"] and not e4_correct:
            categories["expected_authority_retrieved_prediction_wrong"].append(case_id)
        if citations_supported and not row["expected_authority_selected"]:
            categories["citation_traceable_but_expected_authority_not_selected"].append(case_id)

    payload = {
        "analysis_version": "e3e4-evidence-augmented-prediction-error-analysis-v1",
        "source": "artifacts/e3_e4_evidence_augmented_evaluation.json",
        "population_n": 30,
        "categories": {
            key: {"count": len(case_ids), "case_ids": case_ids}
            for key, case_ids in categories.items()
        },
        "interpretation": (
            "Categories are computed from real E3/E4 outcome labels on the frozen 30-case subset. "
            "Zero counts are measured zeros, not structurally inapplicable categories."
        ),
    }
    json_path = ROOT / "artifacts/e3_e4_prediction_error_analysis.json"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# E3/E4 Evidence-Augmented Prediction Error Analysis",
        "",
        "This analysis uses real E3/E4 outcome predictions on the frozen 30-case answer-key subset. Zero-count categories are measured zeros, not structurally inapplicable categories.",
        "",
        "| Category | Count | Cases |",
        "|---|---:|---|",
    ]
    for name, value in payload["categories"].items():
        case_text = ", ".join(f"`{case_id}`" for case_id in value["case_ids"]) or "None"
        lines.append(f"| {name.replace('_', ' ')} | {value['count']}/30 | {case_text} |")
    lines.extend(["", "No canonical E4-minus-E3 prediction-delta metric is defined or reported.", ""])
    markdown_path = ROOT / "artifacts/e3_e4_prediction_error_analysis.md"
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(payload["categories"], indent=2))


if __name__ == "__main__":
    main()
