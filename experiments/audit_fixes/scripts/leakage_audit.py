"""Retrieval leakage / self-match audit for the frozen 30-case E3/E4 cohort.

For each evaluation query:
- query_case_id, query_year
- dedup exclusion set size (audited ILDC->eCourts near cases)
- selected top-5 source_ids / chunk_ids
- self-match flags: selected source in exclusion set? canonical ID equal? temporal violation?
- whether self-match could affect Recall@5/100 (authority recall, not query recall)

Reads only frozen artifacts, no DB required.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, "src")
from legal_xai.retrieval import canonical_case_id

ROOT = Path("/repo")
answer_key = json.loads((ROOT / "answer_key/authority_answer_key.json").read_text(encoding="utf-8"))
entries = [e for e in answer_key["entries"] if e.get("status") == "evaluation"]
eval_ids = sorted(str(e["query_case_id"]) for e in entries)
entry_by_id = {str(e["query_case_id"]): e for e in entries}

# Dedup map: ildc_id -> set(ecourts_case_id, source_id)
dedup_by_ildc: dict[str, set[str]] = {}
with open(ROOT / "corpus/dedup_matches.csv", encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        ildc = str(row.get("ildc_id", "")).strip()
        eco = str(row.get("ecourts_case_id", "")).strip()
        src = str(row.get("source_id", "")).strip()
        if not ildc:
            continue
        s = dedup_by_ildc.setdefault(ildc, set())
        if eco:
            s.add(eco)
        if src:
            s.add(src)

e3e4 = json.loads((ROOT / "artifacts/e3_e4_evidence_augmented_evaluation.json").read_text(encoding="utf-8"))
recs = {str(r["query_case_id"]): r for r in e3e4["per_case_records"]}

print(f"eval_n={len(eval_ids)} per_case_n={len(recs)}")
mismatch_ids = sorted(set(eval_ids) - set(recs))
print(f"missing_in_replay={mismatch_ids}")

self_in_selected = 0
temporal_violations = 0
exclusion_coverage = 0
rows = []
for qid in eval_ids:
    e = entry_by_id[qid]
    qyear = int(str(e["query_decision_date"])[:4])
    r = recs[qid]
    selected = r["E3"]["selected_evidence"]
    excl = dedup_by_ildc.get(qid, set())
    if excl:
        exclusion_coverage += 1
    qcanon = canonical_case_id(qid)
    hits = []
    tvo = 0
    for s in selected:
        src = str(s.get("source_id", ""))
        chunk = str(s.get("chunk_id", ""))
        case = str(s.get("case_id", ""))
        ddate = str(s.get("decision_date", ""))
        dyear = int(ddate[:4]) if len(ddate) >= 4 and ddate[:4].isdigit() else None
        in_excl = src in excl or case in excl
        canon_match = canonical_case_id(case) == qcanon and qcanon is not None
        is_temporal_violation = dyear is not None and dyear >= qyear
        if is_temporal_violation:
            tvo += 1
        if in_excl or canon_match:
            hits.append({"chunk_id": chunk, "source_id": src, "case_id": case,
                         "in_dedup_exclusion": in_excl, "canonical_match": canon_match})
    if hits:
        self_in_selected += 1
    temporal_violations += tvo
    rows.append({"query_case_id": qid, "query_year": qyear,
                 "query_canonical": qcanon,
                 "dedup_exclusion_n": len(excl),
                 "selected_n": len(selected),
                 "self_hits": hits,
                 "temporal_violations": tvo,
                 "recall_at_5": r.get("expected_authority_retrieved_at_5"),
                 "recall_at_100": r.get("expected_authority_retrieved_at_100")})

print(f"queries_with_dedup_exclusion={exclusion_coverage}/30")
print(f"queries_with_self_in_top5={self_in_selected}/30")
print(f"temporal_violations_in_top5={temporal_violations}")
# Recall denominators from frozen artifact (authority recall, not query recall)
print(f"frozen Recall@5={e3e4['E3_retrieval']['recall_at_5']} Recall@100={e3e4['E3_retrieval']['recall_at_100']}")
print(f"provenance_validity={e3e4['E3_retrieval']['citation_provenance_validity']} groundedness={e3e4['E3_retrieval']['citation_groundedness_rate']}")
out = {"eval_n": len(eval_ids),
       "queries_with_dedup_exclusion": exclusion_coverage,
       "queries_with_self_in_top5": self_in_selected,
       "temporal_violations_in_top5": temporal_violations,
       "frozen_recall_at_5": e3e4["E3_retrieval"]["recall_at_5"],
       "frozen_recall_at_100": e3e4["E3_retrieval"]["recall_at_100"],
       "self_match_allowed": "No: dedup exclusion + direct-content 100-phrase/80%-coverage rule + strict earlier-year temporal preranking; query recall is not a metric (authority recall only)",
       "per_query": rows}
Path("/out/leakage_audit.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("wrote /out/leakage_audit.json")
# Print any self-hits detail (should be empty)
for row in rows:
    if row["self_hits"] or row["temporal_violations"]:
        print(json.dumps(row, indent=2))
