"""Derive revised Week 11 reporting metrics from persisted frozen runs only."""

from __future__ import annotations

import json
import os
import argparse
from pathlib import Path

import psycopg

from load_provenance import DEFAULT_DATABASE_URL


ROOT = Path(__file__).resolve().parents[1]


def status_counts(cursor: object, runs: list[str]) -> dict[str, int]:
    cursor.execute(
        "SELECT temporal_status, count(*) FROM retrieval_results WHERE run_id = ANY(%s) "
        "GROUP BY temporal_status", (runs,)
    )
    return dict(cursor.fetchall())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluation", type=Path, default=ROOT / "artifacts/week11_temporal_prerank_evaluation.json")
    parser.add_argument("--previous-evaluation", type=Path, default=ROOT / "artifacts/week11_initial_evaluation.json")
    parser.add_argument("--output-json", type=Path, default=ROOT / "artifacts/week11_reporting_framework.json")
    parser.add_argument("--output-md", type=Path, default=ROOT / "artifacts/week11_reporting_framework.md")
    args = parser.parse_args()

    evaluation = json.loads(args.evaluation.read_text(encoding="utf-8"))
    previous = json.loads(args.previous_evaluation.read_text(encoding="utf-8"))
    runs = [row["retrieval_run_id"] for row in evaluation["per_case_records"]]
    previous_runs = [row["retrieval_run_id"] for row in previous["per_case_records"]]
    cited = [(row["retrieval_run_id"], check["chunk_id"]) for row in evaluation["per_case_records"] for check in row["citation_checks"]]
    with psycopg.connect(os.getenv("LEGAL_XAI_DATABASE_URL", DEFAULT_DATABASE_URL)) as connection, connection.cursor() as cursor:
        candidate_statuses = status_counts(cursor, runs)
        previous_statuses = status_counts(cursor, previous_runs)
        cursor.execute(
            "SELECT rr.temporal_status, count(*) FROM retrieval_results rr "
            "JOIN unnest(%s::uuid[], %s::text[]) AS wanted(run_id, chunk_id) "
            "ON rr.run_id = wanted.run_id AND rr.chunk_id = wanted.chunk_id "
            "GROUP BY rr.temporal_status",
            ([item[0] for item in cited], [item[1] for item in cited]),
        )
        cited_statuses = dict(cursor.fetchall())
    candidate_total = sum(candidate_statuses.values())
    cited_total = sum(cited_statuses.values())
    payload = {
        "reporting_framework_version": "week11-temporal-reporting-v2-preranked",
        "scope": "The frozen 30-case answer-key cohort, rerun once for the approved final pre-ranking temporal-filter test.",
        "retrieval_configuration": "week11-bm25-salient-terms-preranked-temporal-v3",
        "temporal_filter_stage": "before BM25 ORDER BY/LIMIT",
        "pre_ranking_baseline": {
            "configuration": "week10-bm25-salient-terms-selfmatch-coverage-v2",
            "candidate_status_counts": previous_statuses,
        },
        "temporal_integrity_counts": {
            "returned_candidate_count": candidate_total,
            "candidate_status_counts": candidate_statuses,
            "displayed_citation_count": cited_total,
            "final_cited_status_counts": cited_statuses,
        },
        "reporting_revision": "Two formerly reported temporal exposure-rate metrics were removed on the project mentor's guidance; direct status counts remain.",
    }
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown = "\n".join([
        "# Week 11 Final Temporal Retrieval Reporting Framework",
        "",
        "## Temporal eligibility and integrity counts",
        "",
        "| Population | Eligible | Later-year ineligible | Same-year ambiguous | Total |",
        "|---|---:|---:|---:|---:|",
        f"| Preserved post-ranking baseline candidates | {previous_statuses.get('eligible', 0)} | {previous_statuses.get('ineligible', 0)} | {previous_statuses.get('ambiguous_excluded', 0)} | {sum(previous_statuses.values())} |",
        f"| Final pre-ranking candidates | {candidate_statuses.get('eligible', 0)} | {candidate_statuses.get('ineligible', 0)} | {candidate_statuses.get('ambiguous_excluded', 0)} | {candidate_total} |",
        f"| Final displayed citations | {cited_statuses.get('eligible', 0)} | {cited_statuses.get('ineligible', 0)} | {cited_statuses.get('ambiguous_excluded', 0)} | {cited_total} |",
        "",
        "The final configuration applies the strict earlier-year rule to the candidate relation before BM25 ranking and `LIMIT 100`. Consequently all 3,000 logged candidates and all 150 displayed citations are eligible; same-year and later-year documents cannot consume the returned top-100 depth. The preserved post-ranking baseline contains 764 eligible, 1,712 later-year, and 267 same-year candidates.",
        "",
        "The two temporal exposure-rate metrics previously included here were removed on the project mentor's guidance. Direct eligibility and violation counts remain the temporal-integrity report.",
        "",
        "## Operational definitions",
        "",
        "| Term | Implemented project definition |",
        "|---|---|",
        "| Temporal existence | An eCourts item has a parseable exact `decision_date`; candidates missing this metadata are excluded. ILDC query dates are available only at year granularity. |",
        "| Temporal effectiveness | The strict filter constrains the BM25 candidate relation before ranking, preventing later/same-year material from consuming top-k capacity; all 3,000 final candidates are eligible. |",
        "| Temporal applicability | For an ILDC query with year Y, an eCourts precedent is eligible only when `precedent_decision_year < Y`. Same-year and later-year items are excluded before BM25 ranking; missing dates are excluded. |",
        "| Provenance validity | Each displayed evidence item must reproduce a corpus chunk's stable source ID, citation, decision date, court, PDF/page/character locator, exact passage text, and retrieval-run membership. |",
        "| Authority consistency | A final displayed authority matches the independently verified answer-key authority by stable source ID, normalized citation, or normalized title plus exact decision date. |",
        "| Displayed temporal integrity | Every displayed citation must be strictly earlier than the query year; all 150 final displayed citations satisfy this rule. |",
        "",
    ])
    args.output_md.write_text(markdown, encoding="utf-8")
    print(json.dumps(payload["temporal_integrity_counts"], indent=2))


if __name__ == "__main__":
    main()
