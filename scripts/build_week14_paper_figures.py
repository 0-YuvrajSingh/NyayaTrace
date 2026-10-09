"""Render the evaluation-plot deliverable (submission/figures) from the finalized evidence inventory."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission/figures"
INVENTORY = ROOT / "artifacts/week14_results_evidence_inventory.json"
FONT = "font-family='Arial, Helvetica, sans-serif'"
INK = "#202124"
MUTED = "#5f6368"
GRID = "#d7dce2"
BLUE = "#2962a3"
ORANGE = "#d97706"
GREEN = "#2e7d32"
RED = "#b3261e"


def esc(value: object) -> str:
    return html.escape(str(value))


def svg_open(title: str, width: int = 1100, height: int = 640) -> list[str]:
    return [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}' role='img' aria-labelledby='title desc'>",
        f"<title id='title'>{esc(title)}</title>",
        f"<desc id='desc'>{esc(title)}</desc>",
        "<rect width='100%' height='100%' fill='white'/>",
        f"<text x='55' y='44' {FONT} font-size='25' font-weight='700' fill='{INK}'>{esc(title)}</text>",
    ]


def text(x: float, y: float, value: str, size: int = 16, fill: str = INK, anchor: str = "start", weight: str = "400") -> str:
    return f"<text x='{x:.1f}' y='{y:.1f}' {FONT} font-size='{size}' font-weight='{weight}' fill='{fill}' text-anchor='{anchor}'>{esc(value)}</text>"


def line(x1: float, y1: float, x2: float, y2: float, color: str = GRID, width: float = 1) -> str:
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{color}' stroke-width='{width}'/>"


def rect(x: float, y: float, width: float, height: float, fill: str) -> str:
    return f"<rect x='{x:.1f}' y='{y:.1f}' width='{width:.1f}' height='{height:.1f}' fill='{fill}'/>"


def write(name: str, lines: list[str]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    path.write_bytes(("\n".join([*lines, "</svg>"]) + "\n").encode("utf-8"))
    return path


def inventory_row(inventory: dict[str, Any], area: str) -> dict[str, Any]:
    return next(row for row in inventory["result_inventory"] if row["area"] == area)


def outcome_figure(inventory: dict[str, Any]) -> Path:
    measures = inventory_row(inventory, "Outcome prediction")["measures"]
    entries = [
        ("E1", measures["E1_accuracy"], measures["E1_macro_f1"]),
        ("E2 mean-logit", measures["E2_mean_logit_accuracy"], measures["E2_mean_logit_macro_f1"]),
        ("E2 majority-vote", measures["E2_majority_vote_accuracy"], measures["E2_majority_vote_macro_f1"]),
        ("Majority baseline", measures["majority_accuracy"], None),
    ]
    left, top, bottom, right = 100, 115, 555, 1050
    lines = svg_open("Outcome prediction on the frozen test population (n=1,503)")
    for tick in range(0, 8):
        value = tick / 10
        y = bottom - (bottom - top) * value / 0.7
        lines.extend([line(left, y, right, y), text(left - 12, y + 5, f"{value:.1f}", 13, MUTED, "end")])
    lines.extend([line(left, top, left, bottom, INK, 1.5), line(left, bottom, right, bottom, INK, 1.5), text(32, 335, "Score", 15, MUTED)])
    group_width = (right - left) / len(entries)
    bar_width = 58
    for index, (label, accuracy, f1) in enumerate(entries):
        center = left + group_width * (index + 0.5)
        for offset, value, color, tag in ((-34, accuracy, BLUE, "Accuracy"), (34, f1, ORANGE, "Macro F1")):
            if value is None:
                continue
            height = (bottom - top) * value / 0.7
            x = center + offset - bar_width / 2
            lines.extend([rect(x, bottom - height, bar_width, height, color), text(x + bar_width / 2, bottom - height - 9, f"{value:.3f}", 13, INK, "middle")])
        lines.extend([text(center, bottom + 27, label, 14, INK, "middle"), text(center, bottom + 47, "(accuracy only)" if f1 is None else "", 12, MUTED, "middle")])
    lines.extend([rect(730, 70, 16, 16, BLUE), text(754, 83, "Accuracy", 14), rect(850, 70, 16, 16, ORANGE), text(874, 83, "Macro F1", 14)])
    return write("week14_figure_a_outcome_prediction.svg", lines)


def retrieval_funnel_figure(inventory: dict[str, Any]) -> Path:
    measures = inventory_row(inventory, "Authority recovery and verified evidence")["measures"]
    selected = measures["retrieved_and_selected"]
    deferred = measures["retrieved_not_selected"]
    absent = measures["absent_at_k100"]
    total = selected + deferred + absent
    lines = svg_open("Expected-authority recovery funnel (n=30)")
    left, width = 130, 820
    rows = [
        ("Answer-key cases", total, total, BLUE, "30/30"),
        ("Found within k=100", selected + deferred, total, GREEN, f"{selected + deferred}/30 = Recall@100 0.50"),
        ("Displayed among five selected sources", selected, total, BLUE, f"{selected}/30 = Recall@5 0.40"),
    ]
    for index, (label, count, denominator, color, value) in enumerate(rows):
        y = 135 + index * 120
        bar_w = width * count / denominator
        lines.extend([text(left, y - 18, label, 18, INK, "start", "500"), rect(left, y, width, 58, "#edf1f5"), rect(left, y, bar_w, 58, color), text(left + bar_w + 16, y + 37, value, 17, INK)])
    y = 500
    lines.extend([
        text(left, y - 18, "Final k=100 breakdown", 18, INK, "start", "500"),
        rect(left, y, width * selected / total, 58, GREEN),
        rect(left + width * selected / total, y, width * deferred / total, 58, ORANGE),
        rect(left + width * (selected + deferred) / total, y, width * absent / total, 58, RED),
        text(left + width * selected / total / 2, y + 36, f"Selected {selected}", 14, "white", "middle", "500"),
        text(left + width * (selected + deferred / 2) / total, y + 36, f"Retrieved only {deferred}", 14, INK, "middle", "500"),
        text(left + width * ((selected + deferred) + absent / 2) / total, y + 36, f"Absent {absent}", 14, "white", "middle", "500"),
    ])
    return write("week14_figure_b_retrieval_funnel.svg", lines)


def investigation_figure(inventory: dict[str, Any]) -> Path:
    data = inventory["retrieval_investigation_visualization"]
    dev = data["development_probe_recall_at_100"]
    base30 = data["base30_eligibility_filter_comparison"]
    lines = svg_open("Retrieval investigation: development probe and Base-30 eligibility-filter comparison", 1200, 680)
    lines.extend([text(60, 82, "Development probe: Recall@100 (n=9)", 18, INK, "start", "500"), text(660, 82, "Base-30 comparison, exploratory (n=30)", 18, INK, "start", "500")])
    for panel_left, panel_right in ((70, 565), (665, 1140)):
        top, bottom = 125, 530
        for tick in range(0, 11, 2):
            value = tick / 10
            y = bottom - (bottom - top) * value
            lines.extend([line(panel_left, y, panel_right, y), text(panel_left - 10, y + 5, f"{value:.1f}", 12, MUTED, "end")])
        lines.extend([line(panel_left, top, panel_left, bottom, INK, 1.5), line(panel_left, bottom, panel_right, bottom, INK, 1.5)])
    dev_width = 62
    for index, row in enumerate(dev):
        x = 125 + index * 110
        rate = row["numerator"] / row["denominator"]
        height = 405 * rate
        lines.extend([rect(x, 530 - height, dev_width, height, BLUE), text(x + dev_width / 2, 530 - height - 8, f"{row['numerator']}/{row['denominator']}", 13, INK, "middle")])
        words = row["stage"].replace("-", " ").split()
        lines.extend([text(x + dev_width / 2, 554, " ".join(words[:2]), 12, INK, "middle"), text(x + dev_width / 2, 572, " ".join(words[2:]), 12, INK, "middle")])
    for index, row in enumerate(base30):
        center = 760 + index * 210
        for offset, value, color in ((-35, row["recall_at_5"], BLUE), (35, row["recall_at_100"], ORANGE)):
            height = 405 * value
            x = center + offset - 28
            lines.extend([rect(x, 530 - height, 56, height, color), text(x + 28, 530 - height - 8, f"{round(value * row['denominator'])}/{row['denominator']}", 13, INK, "middle")])
        lines.extend([text(center, 554, row["stage"].split()[0], 12, INK, "middle"), text(center, 572, " ".join(row["stage"].split()[1:]), 12, INK, "middle")])
    lines.extend([
        rect(790, 610, 14, 14, BLUE), text(812, 622, "Recall@5 (displayed sources)", 13),
        rect(1000, 610, 14, 14, ORANGE), text(1022, 622, "Recall@100", 13),
        text(70, 642, "Panels use different populations. Base-30 informed configuration choices, so the right panel is exploratory;", 13, MUTED),
        text(70, 660, "its direction is constrained by construction (identical BM25 scores and order for eligible candidates).", 13, MUTED),
    ])
    return write("week14_figure_c_retrieval_investigation.svg", lines)


def integrity_figure(inventory: dict[str, Any]) -> Path:
    measures = inventory_row(inventory, "Authority recovery and verified evidence")["measures"]
    lines = svg_open("Displayed-evidence integrity under the final frozen configuration (n=30)", 1100, 475)
    headers = ["Check", "Result", "Interpretation"]
    rows = [
        ("Citation grounding", "150/150 passed", "Every displayed citation maps to supplied evidence"),
        ("Provenance validity", "150/150 passed", "Every displayed citation has persisted provenance"),
        ("Temporal violations", "0", "No same-year or later authority reached final output"),
        ("Unsupported claims", "0", "Controlled renderer made no unsupported evidence claim"),
    ]
    x = [55, 355, 575, 1045]
    y, row_h = 120, 65
    lines.extend([rect(x[0], y, x[-1] - x[0], row_h, BLUE)])
    for index, header in enumerate(headers):
        lines.append(text(x[index] + 12, y + 41, header, 16, "white", "start", "500"))
    for index, row in enumerate(rows, start=1):
        yy = y + index * row_h
        lines.extend([rect(x[0], yy, x[-1] - x[0], row_h, "#f7f9fb" if index % 2 else "#ffffff"), line(x[0], yy + row_h, x[-1], yy + row_h)])
        for cell, xx in zip(row, x):
            lines.append(text(xx + 12, yy + 41, cell, 15, INK))
    lines.append(text(55, 427, "Final E4 results on displayed evidence (not expected-authority recovery); partly constrained by the extract-only design.", 14, MUTED))
    return write("week14_figure_d_integrity_summary.svg", lines)


def review_figure(inventory: dict[str, Any]) -> Path:
    measures = inventory_row(inventory, "Explanation-format review")["measures"]
    structured = measures["structured_mean_ratings"]
    unstructured = measures["unstructured_mean_ratings"]
    fields = [("Source clarity", "source_clarity"), ("Source-finding ease", "source_finding_ease"), ("Appropriate trust", "appropriate_trust"), ("Limits clear", "limits_clear")]
    left, top, bottom, right = 105, 115, 540, 1050
    lines = svg_open("Explanation-format ratings: author self-review only (n=7)")
    for tick in range(0, 6):
        y = bottom - (bottom - top) * tick / 5
        lines.extend([line(left, y, right, y), text(left - 10, y + 5, str(tick), 13, MUTED, "end")])
    lines.extend([line(left, top, left, bottom, INK, 1.5), line(left, bottom, right, bottom, INK, 1.5), text(42, 330, "Mean rating (1–5)", 15, MUTED)])
    group = (right - left) / len(fields)
    for index, (label, key) in enumerate(fields):
        center = left + group * (index + 0.5)
        for offset, value, color in ((-34, structured[key], BLUE), (34, unstructured[key], ORANGE)):
            height = (bottom - top) * value / 5
            x = center + offset - 27
            lines.extend([rect(x, bottom - height, 54, height, color), text(x + 27, bottom - height - 8, f"{value:.2f}", 13, INK, "middle")])
        words = label.split()
        lines.extend([text(center, bottom + 28, " ".join(words[:2]), 13, INK, "middle"), text(center, bottom + 46, " ".join(words[2:]), 13, INK, "middle")])
    lines.extend([rect(690, 69, 16, 16, BLUE), text(714, 82, "Structured", 14), rect(825, 69, 16, 16, ORANGE), text(849, 82, "Unstructured", 14), text(105, 603, "Descriptive author self-review fallback; not independent human-review evidence.", 14, MUTED)])
    return write("week14_figure_e_explanation_review.svg", lines)


def captions() -> str:
    return """# Figure captions (submission/figures)

Generated by `scripts/build_week14_paper_figures.py` from `artifacts/week14_results_evidence_inventory.json`.
These evaluation plots are a project deliverable; the six-page paper embeds no figures.

**Figure A. Outcome-prediction comparison on the frozen eligible ILDC test population (n=1,503).** E1, E2 mean-logit pooling, E2 majority-vote pooling, and the majority baseline are shown for accuracy and, where applicable, macro F1.

**Figure B. Expected-authority recovery funnel on the 30-case source-verified answer key (n=30).** Under the final pre-ranking configuration, 15/30 expected authorities are found within k=100 and 12/30 are displayed among the five selected sources (Recall@5); the stacked row separates 12 selected, three retrieved-but-unselected, and 15 absent authorities.

**Figure C. Retrieval investigation.** The left panel shows development-probe Recall@100 (n=9, train/validation cases) across the first-32-term query, salient-term query construction, coverage-qualified self-match repair, and a pre-ranking check run after adoption. The right panel shows the Base-30 comparison of the post-ranking and pre-ranking eligibility filters: Recall@5 over displayed sources 11/30 to 12/30, Recall@100 12/30 to 15/30. Base-30 informed configuration choices, so this comparison is exploratory, and its direction is constrained by construction (docs/RQ1_FINAL_ADJUDICATION.md).

**Figure D. Displayed-evidence integrity under the final frozen configuration (n=30 queries; 150 displayed citations).** All displayed citations passed grounding and provenance checks, with zero temporal violations and no unsupported-claim detections. These results are partly constrained by the extract-only design; no unconstrained comparison arm was evaluated.

**Figure E. Explanation-format rubric means from the Week 13 author self-review fallback (n=7 paired cases).** Descriptive self-review only; human-rated explanation quality (RQ3) was not evaluated.
"""


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    paths = [
        outcome_figure(inventory),
        retrieval_funnel_figure(inventory),
        investigation_figure(inventory),
        integrity_figure(inventory),
        review_figure(inventory),
    ]
    (OUT / "captions.md").write_bytes(captions().encode("utf-8"))
    print(json.dumps({"figures": [str(path.relative_to(ROOT)).replace("\\", "/") for path in paths], "status": "figures_and_captions_written"}, indent=2))


if __name__ == "__main__":
    main()
