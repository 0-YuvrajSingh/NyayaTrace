"""Evaluate E3/E4 evidence-augmented prediction on the frozen 30-case subset."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

from build_bm25_index import INDEX_VERSION
from legal_xai.citation_verifier import CitationCheck, RetrievedCandidate, evaluate_against_answer_key
from legal_xai.evidence_augmented_prediction import EvidenceAugmentedPredictor
from legal_xai.evidence_pipeline import retrieve_temporal_candidates, select_diverse_evidence
from legal_xai.facts import extract_case_facts, facts_input_is_eligible, load_facts_extraction_rule
from legal_xai.grounded_answer import assert_answer_grounded, render_grounded_answer
from load_provenance import DEFAULT_DATABASE_URL
from run_grounded_answer_pipeline import verify_rendered_explanation
from run_week11_initial_evaluation import f1, ratio, source_records


def prediction_metrics(labels: list[int], predictions: list[int]) -> dict[str, object]:
    return {
        "n": len(labels),
        "accuracy": round(float(accuracy_score(labels, predictions)), 6),
        "macro_f1": round(float(f1_score(labels, predictions, average="macro", zero_division=0)), 6),
        "confusion_matrix_labels": [0, 1],
        "confusion_matrix": confusion_matrix(labels, predictions, labels=[0, 1]).tolist(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answer-key", type=Path, default=Path("answer_key/authority_answer_key.json"))
    parser.add_argument("--test-split", type=Path, default=Path("corpus/ildc/single_test.parquet"))
    parser.add_argument("--selection-config", type=Path, default=Path("config/evidence_selection.json"))
    parser.add_argument(
        "--prediction-config",
        type=Path,
        default=Path("config/e3_e4_evidence_augmented_prediction.json"),
    )
    parser.add_argument("--facts-config", type=Path, default=Path("config/facts_extraction.json"))
    parser.add_argument("--index", type=Path, default=Path("retrieval/bm25.sqlite"))
    parser.add_argument("--dedup-matches", type=Path, default=Path("corpus/dedup_matches.csv"))
    parser.add_argument("--database-url", default=os.getenv("LEGAL_XAI_DATABASE_URL", DEFAULT_DATABASE_URL))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/e3_e4_evidence_augmented_evaluation.json"),
    )
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.force:
        raise FileExistsError(f"{args.output} already exists; use --force only for an intentional replay")

    answer_key = json.loads(args.answer_key.read_text(encoding="utf-8"))
    selection = json.loads(args.selection_config.read_text(encoding="utf-8"))
    prediction_config = json.loads(args.prediction_config.read_text(encoding="utf-8"))
    entries = [entry for entry in answer_key["entries"] if entry.get("status") == "evaluation"]
    if len(entries) != 30:
        raise ValueError(f"expected the frozen 30-case answer-key subset, found {len(entries)}")
    entry_by_id = {str(entry["query_case_id"]): entry for entry in entries}
    if len(entry_by_id) != len(entries):
        raise ValueError("answer key contains duplicate evaluation case IDs")

    table = pq.read_table(args.test_split, columns=["id", "text", "label"])
    test_rows = {str(row["id"]): row for row in table.to_pylist()}
    missing = sorted(set(entry_by_id) - set(test_rows))
    if missing:
        raise ValueError(f"answer-key cases missing from frozen test split: {missing}")

    predictor = EvidenceAugmentedPredictor(prediction_config)
    facts_rule = load_facts_extraction_rule(args.facts_config)
    records: list[dict[str, Any]] = []
    labels: list[int] = []
    e3_predictions: list[int] = []
    e4_predictions: list[int] = []
    totals = {
        "expected": 0,
        "retrieved_at_5": 0,
        "retrieved_at_100": 0,
        "selected_expected": 0,
        "selected_total": 0,
        "citation_checks": 0,
        "citation_checks_passed": 0,
        "answers_all_citations_passed": 0,
        "temporal_violations": 0,
        "unsupported_answers": 0,
    }

    for case_id, entry in entry_by_id.items():
        source_text = str(test_rows[case_id]["text"] or "")
        facts = extract_case_facts(source_text, facts_rule)
        if not facts_input_is_eligible(facts, facts_rule):
            raise ValueError(f"answer-key case {case_id} is ineligible under the frozen facts rule")
        true_label = int(test_rows[case_id]["label"])
        query_year = int(str(entry["query_decision_date"])[:4])

        retrieved = retrieve_temporal_candidates(
            query_id=case_id,
            query_year=query_year,
            query=facts.text,
            candidate_k=int(selection["candidate_k"]),
            index_path=args.index,
            database_url=args.database_url,
            dedup_matches=args.dedup_matches,
            index_version=f"{INDEX_VERSION};{selection['selection_version']};{prediction_config['config_id']}",
            query_mode="salient_tfidf",
        )
        selected = select_diverse_evidence(retrieved.candidates, int(selection["max_selected_evidence"]))

        # E3 predicts immediately after evidence selection.
        e3_prediction = predictor.predict(facts_text=facts.text, selected_evidence=selected).as_dict()

        # E4 renders and verifies first, then calls the identical shared predictor.
        answer = render_grounded_answer(query=facts.text, selected_evidence=selected).as_dict()
        unsupported = False
        try:
            assert_answer_grounded(answer, selected)
        except AssertionError:
            unsupported = True
        checks = verify_rendered_explanation(
            answer=answer,
            run_id=retrieved.run_id,
            query_id=case_id,
            query_year=query_year,
            database_url=args.database_url,
            dedup_matches=args.dedup_matches,
        )
        e4_prediction = predictor.predict(facts_text=facts.text, selected_evidence=selected).as_dict()
        if e3_prediction != e4_prediction:
            raise RuntimeError(f"E3/E4 shared-predictor parity failed for {case_id}")

        check_objects = tuple(
            CitationCheck(
                evidence_id=check["evidence_id"],
                chunk_id=check["chunk_id"],
                citation=check["citation"],
                passed=bool(check["passed"]),
                failures=tuple(check["failures"]),
            )
            for check in checks
        )
        provenance = source_records(retrieved.candidates, args.database_url)
        candidate_records = tuple(
            RetrievedCandidate(record=provenance[candidate.chunk_id], rank=candidate.rank)
            for candidate in retrieved.candidates
            if candidate.chunk_id in provenance
        )
        retrieval_measure = evaluate_against_answer_key(
            query_id=case_id,
            checks=(),
            answer_key_entries=entries,
            retrieved_candidates=candidate_records,
        )
        selected_measure = evaluate_against_answer_key(
            query_id=case_id,
            checks=check_objects,
            answer_key_entries=entries,
            retrieved_candidates=candidate_records,
        )
        expected = len(retrieval_measure["expected_authority_citations"])
        retrieved_at_5 = any(
            item["rank"] <= 5
            for detail in retrieval_measure["retrieved_expected_authority_details"]
            for item in detail["matches"]
        )
        retrieved_at_100 = bool(retrieval_measure["expected_authorities_retrieved"])
        selected_expected = bool(selected_measure["matched_expected_authorities"])
        passed_checks = sum(bool(check["passed"]) for check in checks)
        temporal_violations = sum(candidate.temporal_status != "eligible" for candidate in selected)

        totals["expected"] += expected
        totals["retrieved_at_5"] += int(retrieved_at_5)
        totals["retrieved_at_100"] += int(retrieved_at_100)
        totals["selected_expected"] += int(selected_expected)
        totals["selected_total"] += len(selected)
        totals["citation_checks"] += len(checks)
        totals["citation_checks_passed"] += passed_checks
        totals["answers_all_citations_passed"] += int(bool(checks) and passed_checks == len(checks))
        totals["temporal_violations"] += temporal_violations
        totals["unsupported_answers"] += int(unsupported)
        labels.append(true_label)
        e3_predictions.append(int(e3_prediction["predicted_label"]))
        e4_predictions.append(int(e4_prediction["predicted_label"]))

        selected_dicts = [candidate.as_dict() for candidate in selected]
        records.append(
            {
                "query_case_id": case_id,
                "query_year": query_year,
                "true_label": true_label,
                "facts_sha256": hashlib.sha256(facts.text.encode("utf-8")).hexdigest(),
                "retrieval_run_id": retrieved.run_id,
                "candidate_count_after_safety_filters": len(retrieved.candidates),
                "expected_authority_retrieved_at_5": retrieved_at_5,
                "expected_authority_retrieved_at_100": retrieved_at_100,
                "expected_authority_selected": selected_expected,
                "expected_authority_retrieved_not_selected": selected_measure[
                    "expected_authorities_retrieved_not_selected"
                ],
                "E3": {
                    "selected_evidence": selected_dicts,
                    "outcome_prediction": e3_prediction,
                },
                "E4": {
                    "evidence": selected_dicts,
                    "provenance": [
                        {
                            key: item[key]
                            for key in (
                                "chunk_id",
                                "source_id",
                                "case_id",
                                "citation",
                                "decision_date",
                                "court",
                                "pdf_file",
                                "page_number",
                                "passage_start_char",
                                "passage_end_char",
                            )
                        }
                        for item in selected_dicts
                    ],
                    "citation_status": {
                        "status": "passed" if passed_checks == len(checks) else "failed",
                        "passed_count": passed_checks,
                        "checks": checks,
                    },
                    "explanation": answer,
                    "outcome_prediction": e4_prediction,
                },
            }
        )

    authority_precision = ratio(totals["selected_expected"], totals["selected_total"])
    authority_recall = ratio(totals["selected_expected"], totals["expected"])
    evidence_metrics = {
        "n": len(labels),
        "recall_at_5": ratio(totals["retrieved_at_5"], totals["expected"]),
        "recall_at_100": ratio(totals["retrieved_at_100"], totals["expected"]),
        "authority_consistent_precision": authority_precision,
        "authority_consistent_recall": authority_recall,
        "authority_consistent_f1": f1(authority_precision, authority_recall),
        "citation_groundedness_rate": ratio(totals["answers_all_citations_passed"], len(labels)),
        "citation_provenance_validity": ratio(totals["citation_checks_passed"], totals["citation_checks"]),
        "temporal_violation_rate": ratio(totals["temporal_violations"], totals["selected_total"]),
        "unsupported_claim_rate": ratio(totals["unsupported_answers"], len(labels)),
        "denominators": {
            "expected_authorities": totals["expected"],
            "selected_evidence_items": totals["selected_total"],
            "displayed_citation_checks": totals["citation_checks"],
        },
    }
    payload = {
        "evaluation_version": "e3e4-evidence-augmented-answer-key-evaluation-v1",
        "prediction_config": prediction_config,
        "population": {
            "n": len(labels),
            "description": "frozen 30-case answer-key-covered subset of the ILDC test split",
        },
        "E3_outcome_prediction": prediction_metrics(labels, e3_predictions),
        "E4_outcome_prediction": prediction_metrics(labels, e4_predictions),
        "E3_retrieval": evidence_metrics,
        "E4_verified_evidence": evidence_metrics,
        "per_case_records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "E3": payload["E3_outcome_prediction"],
                "E4": payload["E4_outcome_prediction"],
                "evidence": evidence_metrics,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
