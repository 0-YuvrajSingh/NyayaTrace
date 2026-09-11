"""RQ2 provenance/citation-validation ablation: condition A (E3, no verification)
vs condition D (full E4) on the read-time 37-case set, plus positive-control
probes of the unchanged verifier (mutated passage / mutated authority /
backdated query year must FAIL).

Additive evaluation-only driver. Frozen retrieval/selection/predictor/verify
functions reused unchanged. Writes ONLY under experiments/rq2/.
"""

from __future__ import annotations

import argparse
import copy
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
from legal_xai.citation_verifier import CitationCheck, RetrievedCandidate, evaluate_against_answer_key, verify_answer_citations
from legal_xai.evidence_augmented_prediction import EvidenceAugmentedPredictor
from legal_xai.evidence_pipeline import retrieve_temporal_candidates, select_diverse_evidence
from legal_xai.facts import extract_case_facts, facts_input_is_eligible, load_facts_extraction_rule
from legal_xai.grounded_answer import assert_answer_grounded, render_grounded_answer
from legal_xai.retrieval import query_exclusion_cases
from load_provenance import DEFAULT_DATABASE_URL
from run_grounded_answer_pipeline import verify_rendered_explanation
from run_week11_initial_evaluation import f1, ratio, source_records
import psycopg
from legal_xai.citation_verifier import CorpusEvidenceRecord

EXPECTED = {"base": "f4ccb0fa8bfc11425988eb0b615b491c9908a97cb9d2c8a5343a14dae8600e81",
            "ext": "afa0329f49afc7041cc824bcbee0e4469097588b03bc3f9009b547bb2ff4495d"}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def pred_metrics(labels, preds) -> dict:
    return {"n": len(labels), "accuracy": round(float(accuracy_score(labels, preds)), 6),
            "macro_f1": round(float(f1_score(labels, preds, average="macro", zero_division=0)), 6),
            "confusion_matrix_labels": [0, 1],
            "confusion_matrix": confusion_matrix(labels, preds, labels=[0, 1]).tolist()}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--answer-key", type=Path, default=Path("answer_key/authority_answer_key.json"))
    ap.add_argument("--extension", type=Path, default=Path("answer_key/extension_v6/verified_7_case_extension.json"))
    ap.add_argument("--test-split", type=Path, default=Path("corpus/ildc/single_test.parquet"))
    ap.add_argument("--selection-config", type=Path, default=Path("config/evidence_selection.json"))
    ap.add_argument("--prediction-config", type=Path, default=Path("config/e3_e4_evidence_augmented_prediction.json"))
    ap.add_argument("--facts-config", type=Path, default=Path("config/facts_extraction.json"))
    ap.add_argument("--index", type=Path, default=Path("retrieval/bm25.sqlite"))
    ap.add_argument("--dedup-matches", type=Path, default=Path("corpus/dedup_matches.csv"))
    ap.add_argument("--database-url", default=os.getenv("LEGAL_XAI_DATABASE_URL", DEFAULT_DATABASE_URL))
    ap.add_argument("--output", type=Path, default=Path("experiments/rq2/rq2_results.json"))
    args = ap.parse_args()

    assert sha(args.answer_key) == EXPECTED["base"], "base key changed - STOP"
    assert sha(args.extension) == EXPECTED["ext"], "extension changed - STOP"
    ak = json.loads(args.answer_key.read_text(encoding="utf-8"))
    entries = [e for e in ak["entries"] if e.get("status") == "evaluation"]
    ext = json.loads(args.extension.read_text(encoding="utf-8"))
    assert len(entries) == 30 and len(ext["extension"]["cases"]) == 7
    mapped = []
    for rec in ext["extension"]["cases"]:
        assert rec["verification_status"] == "VERIFIED"
        ai = rec["authority_identity"]
        mapped.append({"status": "evaluation", "query_case_id": rec["candidate_case_id"],
                       "query_year": rec["query_year"], "authority_source_id": ai["source_id"],
                       "authority_citation": rec["authority_citation"], "authority_title": ai["title"],
                       "authority_decision_date": ai["decision_date"], "stratum": "extension7"})
    for e in entries:
        e["stratum"] = "base30"
    all_entries = entries + mapped
    assert len(all_entries) == 37
    by_id = {str(e["query_case_id"]): e for e in all_entries}
    assert len(by_id) == 37

    selection = json.loads(args.selection_config.read_text(encoding="utf-8"))
    prediction_config = json.loads(args.prediction_config.read_text(encoding="utf-8"))
    table = pq.read_table(args.test_split, columns=["id", "text", "label"])
    test_rows = {str(r["id"]): r for r in table.to_pylist()}
    predictor = EvidenceAugmentedPredictor(prediction_config)
    facts_rule = load_facts_extraction_rule(args.facts_config)

    rows: list[dict] = []
    probe_totals = {"passage_mutation": [0, 0], "authority_mutation": [0, 0], "temporal_backdate": [0, 0]}
    for case_id, entry in sorted(by_id.items()):
        text = str(test_rows[case_id]["text"] or "")
        facts = extract_case_facts(text, facts_rule)
        assert facts_input_is_eligible(facts, facts_rule)
        true_label = int(test_rows[case_id]["label"])
        qy = int(str(entry["query_decision_date"])[:4]) if "query_decision_date" in entry else int(entry["query_year"])
        retrieved = retrieve_temporal_candidates(
            query_id=case_id, query_year=qy, query=facts.text, candidate_k=int(selection["candidate_k"]),
            index_path=args.index, database_url=args.database_url, dedup_matches=args.dedup_matches,
            index_version=f"{INDEX_VERSION};{selection['selection_version']};rq2-ablation-v1",
            query_mode="salient_tfidf")
        selected = select_diverse_evidence(retrieved.candidates, int(selection["max_selected_evidence"]))
        # Condition A: E3 branch (selection only, zero checks).
        e3_pred = predictor.predict(facts_text=facts.text, selected_evidence=selected).as_dict()
        # Condition D: E4 branch (render + assert + verify, fail-closed).
        answer = render_grounded_answer(query=facts.text, selected_evidence=selected).as_dict()
        unsupported = False
        try:
            assert_answer_grounded(answer, selected)
        except AssertionError:
            unsupported = True
        try:
            checks = verify_rendered_explanation(answer=answer, run_id=retrieved.run_id, query_id=case_id,
                                                 query_year=qy, database_url=args.database_url,
                                                 dedup_matches=args.dedup_matches)
            d_failed, d_failures = False, []
        except ValueError as exc:
            checks, d_failed, d_failures = [], True, [str(exc)[:300]]
        e4_pred = predictor.predict(facts_text=facts.text, selected_evidence=selected).as_dict()
        assert e3_pred == e4_pred, f"predictor parity failed for {case_id}"
        passed = sum(bool(c["passed"]) for c in checks)
        # Positive controls through the UNCHANGED verifier.
        with psycopg.connect(args.database_url) as conn, conn.cursor() as cur:
            cur.execute("SELECT chunk_id, source_id, case_id, citation, decision_date, title, court, pdf_file, "
                        "page_number, passage_start_char, passage_end_char, chunk_text FROM corpus_chunks "
                        "WHERE chunk_id = ANY(%s)", ([i["chunk_id"] for i in answer.get("supporting_evidence", [])],))
            records = {r[0]: CorpusEvidenceRecord(chunk_id=r[0], source_id=r[1], case_id=r[2], citation=r[3],
                       decision_date=r[4].isoformat(), title=r[5], court=r[6], pdf_file=r[7], page_number=r[8],
                       passage_start_char=r[9], passage_end_char=r[10], text=r[11]) for r in cur.fetchall()}
            cur.execute("SELECT chunk_id FROM retrieval_results WHERE run_id = %s AND temporal_status = 'eligible'",
                        (retrieved.run_id,))
            run_ids = {r[0] for r in cur.fetchall()}
        near = query_exclusion_cases(case_id, args.dedup_matches)
        probes = {}
        if answer.get("supporting_evidence"):
            mut = copy.deepcopy(answer)
            ev0 = mut["supporting_evidence"][0]
            ev0["verbatim_passage"] = (ev0.get("verbatim_passage") or "") + " [MUTATED]"
            r1 = verify_answer_citations(answer=mut, query_id=case_id, query_year=qy, corpus_records=records,
                                         retrieved_chunk_ids=run_ids, audited_near_case_ids=near)
            probes["passage_mutation_rejected"] = not all(c.passed for c in r1)
            mut2 = copy.deepcopy(answer)
            mut2["applicable_law_and_cases"][0]["citation"] = "FABRICATED 9999 XYZ 0"
            r2 = verify_answer_citations(answer=mut2, query_id=case_id, query_year=qy, corpus_records=records,
                                         retrieved_chunk_ids=run_ids, audited_near_case_ids=near)
            probes["authority_mutation_rejected"] = not all(c.passed for c in r2)
            auth_year = min(int(v.decision_date[:4]) for v in records.values()) if records else qy
            r3 = verify_answer_citations(answer=answer, query_id=case_id, query_year=auth_year - 1,
                                         corpus_records=records, retrieved_chunk_ids=run_ids,
                                         audited_near_case_ids=near)
            probes["temporal_backdate_rejected"] = not all(c.passed for c in r3)
        else:
            probes = {"passage_mutation_rejected": None, "authority_mutation_rejected": None,
                      "temporal_backdate_rejected": None}
        for k, short in (("passage_mutation_rejected", "passage_mutation"),
                         ("authority_mutation_rejected", "authority_mutation"),
                         ("temporal_backdate_rejected", "temporal_backdate")):
            if probes[k] is not None:
                probe_totals[short][1] += 1
                probe_totals[short][0] += int(probes[k])
        rows.append({
            "query_case_id": case_id, "stratum": entry.get("stratum"), "query_year": qy, "true_label": true_label,
            "expected_authority": entry.get("authority_citation"),
            "a_selected_ids": [c.chunk_id for c in selected], "a_n_evidence": len(selected),
            "a_checks_performed": 0,
            "d_n_checks": len(checks), "d_checks_passed": passed,
            "d_all_passed": bool(checks) and passed == len(checks),
            "d_failed_closed": d_failed, "d_failures": d_failures,
            "d_temporal_violations": sum(c.temporal_status != "eligible" for c in selected),
            "d_unsupported": unsupported,
            "d_rejected_items": len(checks) - passed,
            "d_changed_output_vs_a": bool(checks) and passed != len(checks),
            "probes": probes,
            "e3_predicted_label": int(e3_pred["predicted_label"]),
            "e4_predicted_label": int(e4_pred["predicted_label"]),
        })

    def stratum_metrics(sub):
        n = len(sub)
        nc = sum(r["d_n_checks"] for r in sub)
        pc = sum(r["d_checks_passed"] for r in sub)
        tv = sum(r["d_temporal_violations"] for r in sub)
        uns = sum(int(r["d_unsupported"]) for r in sub)
        rej = sum(r["d_rejected_items"] for r in sub)
        allt = sum(int(r["d_all_passed"]) for r in sub)
        return {
            "n": n,
            "a_checks_performed": 0,
            "d_citation_groundedness_rate": {"num": allt, "den": n, "value": ratio(allt, n)},
            "d_citation_provenance_validity": {"num": pc, "den": nc, "value": ratio(pc, nc)},
            "d_temporal_violation_rate": {"num": tv, "den": sum(r["a_n_evidence"] for r in sub), "value": ratio(tv, sum(r["a_n_evidence"] for r in sub))},
            "d_unsupported_claim_rate": {"num": uns, "den": n, "value": ratio(uns, n)},
            "d_rejected_items_total": rej,
            "cases_where_d_rejected": sum(int(r["d_rejected_items"] > 0) for r in sub),
            "e3_prediction": pred_metrics([r["true_label"] for r in sub], [r["e3_predicted_label"] for r in sub]),
            "e4_prediction": pred_metrics([r["true_label"] for r in sub], [r["e4_predicted_label"] for r in sub]),
        }

    payload = {
        "rq": "RQ2: provenance/citation/temporal controls (A=E3 unverified vs D=full E4) on the frozen 37-case set",
        "evaluation_version": "rq2-ablation-37-case-v1",
        "conditions": {"A": "E3 selection only; zero verification checks (frozen E3 path)",
                       "D": "full E4: render + assert + 5-check verifier, fail-closed (frozen E4 path)"},
        "reference_set": {"base_cases": 30, "extension_cases": 7, "combined_cases": 37},
        "positive_control_probes": {k: {"rejected": v[0], "denominator": v[1]} for k, v in probe_totals.items()},
        "strata": {name: stratum_metrics([r for r in rows if f(r)]) for name, f in
                   (("base30", lambda r: r["stratum"] == "base30"),
                    ("extension7", lambda r: r["stratum"] == "extension7"),
                    ("combined37", lambda r: True))},
        "per_case_rows": [{k: v for k, v in r.items()} for r in rows],
        "run_manifest": {"baseline_commit": "2bd02b3", "baseline_tag": "v4-baseline-reproduced",
                         "run_at_utc": datetime.now(UTC).isoformat(), "python": sys.version.split()[0],
                         "platform": platform.platform(),
                         "command": "run_rq2_37.py --output experiments/rq2/rq2_results.json (container nyayatrace-e2:repro --gpus all)"},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "combined37": payload["strata"]["combined37"],
                      "probes": payload["positive_control_probes"]}, indent=2))


if __name__ == "__main__":
    main()
