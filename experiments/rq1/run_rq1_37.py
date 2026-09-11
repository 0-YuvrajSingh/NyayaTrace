"""RQ1 evaluation on the logical 37-case reference set (30 frozen + 7 verified extension).

Additive evaluation-only driver. Reuses the frozen E3 implementation path
(retrieve -> select -> shared predictor) with frozen configs. The existing
30-case script hard-codes its population (len(entries) != 30 raises), so it
cannot read the additive set; this driver assembles the 37 entries AT READ
TIME from the two immutable sources without rewriting either JSON.

Writes ONLY under experiments/rq1/. Never touches frozen artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path

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

EXPECTED_BASE_SHA = "f4ccb0fa8bfc11425988eb0b615b491c9908a97cb9d2c8a5343a14dae8600e81"
EXPECTED_EXT_SHA = "afa0329f49afc7041cc824bcbee0e4469097588b03bc3f9009b547bb2ff4495d"
EXPECTED_VRES_SHA = "8939dba56b714449bfe540ce7c50f949bb9b2282ab9355a1b27633a12016a1d9"
EXPECTED_PROMOTED = ["1990_234", "1990_256", "1990_324", "1991_136", "1991_87", "1992_286", "1993_90"]
EXCLUDED_REVIEW = ["1991_198", "1993_89", "1990_188"]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def prediction_metrics(labels: list[int], predictions: list[int]) -> dict:
    return {
        "n": len(labels),
        "accuracy": round(float(accuracy_score(labels, predictions)), 6),
        "macro_f1": round(float(f1_score(labels, predictions, average="macro", zero_division=0)), 6),
        "confusion_matrix_labels": [0, 1],
        "confusion_matrix": confusion_matrix(labels, predictions, labels=[0, 1]).tolist(),
    }


def evidence_metrics(rows: list[dict]) -> dict:
    t = {"expected": 0, "retrieved_at_5": 0, "retrieved_at_100": 0, "selected_expected": 0,
         "selected_total": 0, "citation_checks": 0, "citation_checks_passed": 0,
         "answers_all": 0, "temporal_violations": 0, "unsupported": 0}
    for r in rows:
        t["expected"] += r["n_expected"]
        t["retrieved_at_5"] += int(r["retrieved_at_5"])
        t["retrieved_at_100"] += int(r["retrieved_at_100"])
        t["selected_expected"] += int(r["selected_expected"])
        t["selected_total"] += r["n_selected"]
        t["citation_checks"] += r["n_checks"]
        t["citation_checks_passed"] += r["n_checks_passed"]
        t["answers_all"] += int(r["all_passed"])
        t["temporal_violations"] += r["temporal_violations"]
        t["unsupported"] += int(r["unsupported"])
    prec = ratio(t["selected_expected"], t["selected_total"])
    rec = ratio(t["selected_expected"], t["expected"])
    return {
        "n": len(rows),
        "recall_at_5": ratio(t["retrieved_at_5"], t["expected"]),
        "recall_at_100": ratio(t["retrieved_at_100"], t["expected"]),
        "authority_consistent_precision": prec,
        "authority_consistent_recall": rec,
        "authority_consistent_f1": f1(prec, rec),
        "citation_groundedness_rate": ratio(t["answers_all"], len(rows)),
        "citation_provenance_validity": ratio(t["citation_checks_passed"], t["citation_checks"]),
        "temporal_violation_rate": ratio(t["temporal_violations"], t["selected_total"]),
        "unsupported_claim_rate": ratio(t["unsupported"], len(rows)),
        "denominators": {"expected_authorities": t["expected"], "selected_evidence_items": t["selected_total"],
                         "displayed_citation_checks": t["citation_checks"]},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--answer-key", type=Path, default=Path("answer_key/authority_answer_key.json"))
    parser.add_argument("--extension", type=Path, default=Path("answer_key/extension_v6/verified_7_case_extension.json"))
    parser.add_argument("--manifest", type=Path, default=Path("answer_key/extension_v6/extension_manifest.json"))
    parser.add_argument("--test-split", type=Path, default=Path("corpus/ildc/single_test.parquet"))
    parser.add_argument("--selection-config", type=Path, default=Path("config/evidence_selection.json"))
    parser.add_argument("--prediction-config", type=Path, default=Path("config/e3_e4_evidence_augmented_prediction.json"))
    parser.add_argument("--facts-config", type=Path, default=Path("config/facts_extraction.json"))
    parser.add_argument("--e2-predictions", type=Path, default=Path("artifacts/e2_test_predictions.json"))
    parser.add_argument("--index", type=Path, default=Path("retrieval/bm25.sqlite"))
    parser.add_argument("--dedup-matches", type=Path, default=Path("corpus/dedup_matches.csv"))
    parser.add_argument("--database-url", default=os.getenv("LEGAL_XAI_DATABASE_URL", DEFAULT_DATABASE_URL))
    parser.add_argument("--output", type=Path, default=Path("experiments/rq1/rq1_results.json"))
    args = parser.parse_args()

    anchors = {"base_key": _sha256(args.answer_key), "extension": _sha256(args.extension)}
    assert anchors["base_key"] == EXPECTED_BASE_SHA, "base 30-case key changed - STOP"
    assert anchors["extension"] == EXPECTED_EXT_SHA, "extension changed - STOP"
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    assert manifest["promoted_case_ids"] == EXPECTED_PROMOTED, "promoted list changed - STOP"

    answer_key = json.loads(args.answer_key.read_text(encoding="utf-8"))
    base_entries = [e for e in answer_key["entries"] if e.get("status") == "evaluation"]
    ext = json.loads(args.extension.read_text(encoding="utf-8"))
    assert base_entries and len(base_entries) == 30, f"base {len(base_entries)} != 30 - STOP"
    assert ext["extension"]["case_count"] == 7 and len(ext["extension"]["cases"]) == 7, "extension != 7 - STOP"
    mapped = []
    for rec in ext["extension"]["cases"]:
        assert rec.get("verification_status") == "VERIFIED", rec["candidate_case_id"]
        assert rec["candidate_case_id"] not in EXCLUDED_REVIEW
        ai = rec["authority_identity"]
        mapped.append({
            "status": "evaluation",  # read-time mapping only; extension JSON itself is untouched
            "query_case_id": rec["candidate_case_id"],
            "query_year": rec["query_year"],
            "query_label": rec["query_label"],
            "authority_source_id": ai["source_id"],
            "authority_citation": rec["authority_citation"],
            "authority_title": ai["title"],
            "authority_decision_date": ai["decision_date"],
            "stratum": "extension7",
            "_mapping": "verification record -> answer-key-shaped entry at read time; see run manifest",
        })
    for e in base_entries:
        e["stratum"] = "base30"
    entries = base_entries + mapped
    assert len(entries) == 37, "combined != 37 - STOP"
    assert {e["query_case_id"] for e in entries} == {e["query_case_id"] for e in base_entries} | set(EXPECTED_PROMOTED)
    entry_by_id = {str(e["query_case_id"]): e for e in entries}
    assert len(entry_by_id) == 37, "duplicate case IDs - STOP"

    selection = json.loads(args.selection_config.read_text(encoding="utf-8"))
    prediction_config = json.loads(args.prediction_config.read_text(encoding="utf-8"))
    table = pq.read_table(args.test_split, columns=["id", "text", "label"])
    test_rows = {str(row["id"]): row for row in table.to_pylist()}
    assert not (set(entry_by_id) - set(test_rows)), "reference cases missing from test split - STOP"

    # E2 side: frozen per-case predictions (already reproduced exactly in baseline phase).
    e2 = json.loads(args.e2_predictions.read_text(encoding="utf-8"))
    e2_by_id = {r["case_id"]: r for r in e2["records"]}
    assert all(cid in e2_by_id for cid in entry_by_id), "E2 predictions missing cases - STOP"

    predictor = EvidenceAugmentedPredictor(prediction_config)
    facts_rule = load_facts_extraction_rule(args.facts_config)
    rows: list[dict] = []
    for case_id, entry in sorted(entry_by_id.items()):
        source_text = str(test_rows[case_id]["text"] or "")
        facts = extract_case_facts(source_text, facts_rule)
        if not facts_input_is_eligible(facts, facts_rule):
            raise ValueError(f"reference case {case_id} ineligible under frozen facts rule")
        true_label = int(test_rows[case_id]["label"])
        if "query_decision_date" in entry:
            qy = int(str(entry["query_decision_date"])[:4])
        else:
            qy = int(entry["query_year"])  # extension records carry year-only (no date invented)
        retrieved = retrieve_temporal_candidates(
            query_id=case_id, query_year=qy, query=facts.text,
            candidate_k=int(selection["candidate_k"]), index_path=args.index,
            database_url=args.database_url, dedup_matches=args.dedup_matches,
            index_version=f"{INDEX_VERSION};{selection['selection_version']};{prediction_config['config_id']}",
            query_mode="salient_tfidf")
        selected = select_diverse_evidence(retrieved.candidates, int(selection["max_selected_evidence"]))
        e3_prediction = predictor.predict(facts_text=facts.text, selected_evidence=selected).as_dict()
        answer = render_grounded_answer(query=facts.text, selected_evidence=selected).as_dict()
        unsupported = False
        try:
            assert_answer_grounded(answer, selected)
        except AssertionError:
            unsupported = True
        checks = verify_rendered_explanation(answer=answer, run_id=retrieved.run_id, query_id=case_id,
                                             query_year=qy, database_url=args.database_url,
                                             dedup_matches=args.dedup_matches)
        e4_prediction = predictor.predict(facts_text=facts.text, selected_evidence=selected).as_dict()
        if e3_prediction != e4_prediction:
            raise RuntimeError(f"E3/E4 shared-predictor parity failed for {case_id}")
        check_objects = tuple(CitationCheck(evidence_id=c["evidence_id"], chunk_id=c["chunk_id"],
                                            citation=c["citation"], passed=bool(c["passed"]),
                                            failures=tuple(c["failures"])) for c in checks)
        provenance = source_records(retrieved.candidates, args.database_url)
        candidate_records = tuple(RetrievedCandidate(record=provenance[c.chunk_id], rank=c.rank)
                                  for c in retrieved.candidates if c.chunk_id in provenance)
        retrieval_measure = evaluate_against_answer_key(query_id=case_id, checks=(), answer_key_entries=entries,
                                                        retrieved_candidates=candidate_records)
        selected_measure = evaluate_against_answer_key(query_id=case_id, checks=check_objects,
                                                       answer_key_entries=entries,
                                                       retrieved_candidates=candidate_records)
        r5 = any(item["rank"] <= 5 for detail in retrieval_measure["retrieved_expected_authority_details"] for item in detail["matches"])
        r100 = bool(retrieval_measure["expected_authorities_retrieved"])
        sel = bool(selected_measure["matched_expected_authorities"])
        passed = sum(bool(c["passed"]) for c in checks)
        rows.append({
            "query_case_id": case_id, "stratum": entry.get("stratum"), "query_year": qy, "true_label": true_label,
            "expected_authority": entry.get("authority_citation"),
            "expected_relationship": entry.get("relationship", "see-extension-record"),
            "retrieval_run_id": retrieved.run_id, "n_expected": len(retrieval_measure["expected_authority_citations"]),
            "retrieved_at_5": r5, "retrieved_at_100": r100, "selected_expected": sel,
            "expected_rank": min(([item["rank"] for detail in retrieval_measure["retrieved_expected_authority_details"] for item in detail["matches"]] or [None])),
            "n_selected": len(selected),
            "selected_source_ids": [c.source_id for c in selected],
            "n_checks": len(checks), "n_checks_passed": passed, "all_passed": bool(checks) and passed == len(checks),
            "temporal_violations": sum(c.temporal_status != "eligible" for c in selected),
            "unsupported": unsupported,
            "e3_predicted_label": int(e3_prediction["predicted_label"]),
            "identity_match_method": "source_id/citation/title+date via frozen _candidate_matches_expected",
        })

    strata = {}
    for name, filt in (("base30", lambda r: r["stratum"] == "base30"),
                       ("extension7", lambda r: r["stratum"] == "extension7"),
                       ("combined37", lambda r: True)):
        sub = [r for r in rows if filt(r)]
        labels = [r["true_label"] for r in sub]
        e3p = [r["e3_predicted_label"] for r in sub]
        e2p = [int(e2_by_id[r["query_case_id"]]["E2_mean_logits_prediction"]) for r in sub]
        e2l = [int(e2_by_id[r["query_case_id"]]["true_label"]) for r in sub]
        assert e2l == labels, f"E2 label mismatch in {name}"
        strata[name] = {"n": len(sub), "e3_retrieval": evidence_metrics(sub),
                        "e3_prediction": prediction_metrics(labels, e3p),
                        "e2_facts_only": prediction_metrics(labels, e2p)}
    payload = {
        "rq": "RQ1: facts-only Legal-BERT (E2) vs facts+BM25-evidence (E3) on the frozen 37-case reference-evidence set",
        "evaluation_version": "rq1-37-case-reference-evidence-v1",
        "reference_set": {"base_cases": 30, "extension_cases": 7, "combined_cases": 37,
                          "base_sha256": anchors["base_key"], "extension_sha256": anchors["extension"],
                          "assembly": "read-time concatenation; both sources unmodified"},
        "controlled_conditions": {"same_cases": True, "same_preprocessing": "ildc-predecision-facts-v1",
            "same_checkpoint": "checkpoint-6318", "same_seed": 202607, "same_corpus": True,
            "same_index": "fts5-bm25-unicode61-temporal-v2", "same_topk": 100, "same_selection": "top5-1-per-source",
            "same_temporal_policy": "precedent_year<query_year pre-rank",
            "controlled_change": "E2 no retrieved evidence; E3 retrieved evidence added"},
        "strata": strata,
        "per_case_rows": [{k: v for k, v in r.items() if k != "retrieval_run_id"} for r in rows],
        "run_manifest": {
            "baseline_commit": "2bd02b3", "baseline_tag": "v4-baseline-reproduced",
            "run_at_utc": datetime.now(UTC).isoformat(), "python": sys.version.split()[0], "platform": platform.platform(),
            "command": "run_rq1_37.py --output experiments/rq1/rq1_results.json (container nyayatrace-e2:repro --gpus all)",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "combined_e3": strata["combined37"]["e3_retrieval"],
                      "combined_e3_pred": strata["combined37"]["e3_prediction"],
                      "combined_e2": strata["combined37"]["e2_facts_only"]}, indent=2))


if __name__ == "__main__":
    main()
