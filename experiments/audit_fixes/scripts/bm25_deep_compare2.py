"""Optimized BM25 deep compare with progress logging.

- Identity via chunk_temporal_metadata (indexed, fast), not FTS count(*) (slow full scan).
- Per-stage flush prints so liveness is visible.
- Production temporal SQL + salient_tfidf for 30 eval queries, per-query verdict prints.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sqlite3
from pathlib import Path
import sys

sys.path.insert(0, "src")
sys.path.insert(0, "scripts")

import pyarrow.parquet as pq

from legal_xai.evidence_pipeline import temporal_preranked_bm25_sql
from legal_xai.facts import extract_case_facts, load_facts_extraction_rule
from legal_xai.retrieval import fts_query


def hash_temporal(db_path: str, label: str) -> tuple[int, str]:
    print(f"[{label}] opening {db_path}", flush=True)
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        n = con.execute("SELECT count(*) FROM chunk_temporal_metadata").fetchone()[0]
        print(f"[{label}] temporal count={n}", flush=True)
        h = hashlib.sha256()
        cur = con.execute("SELECT chunk_id FROM chunk_temporal_metadata ORDER BY chunk_id")
        done = 0
        for (cid,) in cur:
            h.update(cid.encode())
            h.update(b"\x00")
            done += 1
            if done % 500000 == 0:
                print(f"[{label}] hashed {done}/{n}", flush=True)
        print(f"[{label}] done hashed={done} sha={h.hexdigest()}", flush=True)
        return n, h.hexdigest()
    finally:
        con.close()


def topk(db_path: str, query: str, year: int, k: int) -> list[str]:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute(temporal_preranked_bm25_sql(), (query, year, k)).fetchall()
        return [r[0] for r in rows]
    finally:
        con.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frozen-db", required=True)
    ap.add_argument("--rebuilt-db", required=True)
    ap.add_argument("--answer-key", default="answer_key/authority_answer_key.json")
    ap.add_argument("--test-split", default="corpus/ildc/single_test.parquet")
    ap.add_argument("--facts-config", default="config/facts_extraction.json")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    f_n, f_hash = hash_temporal(args.frozen_db, "frozen")
    r_n, r_hash = hash_temporal(args.rebuilt_db, "rebuilt")
    print(f"chunk_identity: {'IDENTICAL' if (f_n == r_n and f_hash == r_hash) else 'DIFFERS'}", flush=True)

    answer_key = json.loads(Path(args.answer_key).read_text(encoding="utf-8"))
    entries = [e for e in answer_key["entries"] if e.get("status") == "evaluation"]
    print(f"eval entries: {len(entries)}", flush=True)
    table = pq.read_table(args.test_split, columns=["id", "text"])
    text_by_id = {str(r["id"]): str(r["text"] or "") for r in table.to_pylist()}
    rule = load_facts_extraction_rule(Path(args.facts_config))

    identical = 0
    mismatch = 0
    per_case = []
    for i, e in enumerate(sorted(entries, key=lambda x: str(x["query_case_id"])), 1):
        cid = str(e["query_case_id"])
        year = int(str(e["query_decision_date"])[:4])
        facts = extract_case_facts(text_by_id[cid], rule)
        q = fts_query(facts.text, mode="salient_tfidf")
        f_top = topk(args.frozen_db, q, year, 100)
        r_top = topk(args.rebuilt_db, q, year, 100)
        verdict = "MATCH" if f_top == r_top else "MISMATCH"
        if verdict == "MATCH":
            identical += 1
        else:
            mismatch += 1
        print(f"[{i}/30] {cid} year={year} -> {verdict} n={len(f_top)}/{len(r_top)}", flush=True)
        per_case.append({"query_case_id": cid, "query_year": year, "verdict": verdict,
                         "frozen_top5": f_top[:5], "rebuilt_top5": r_top[:5]})

    overall = "MATCH" if mismatch == 0 else "MISMATCH"
    summary = {"frozen_temporal_count": f_n, "rebuilt_temporal_count": r_n,
               "chunk_id_ordered_sha256_frozen": f_hash,
               "chunk_id_ordered_sha256_rebuilt": r_hash,
               "chunk_identity": "IDENTICAL" if (f_n == r_n and f_hash == r_hash) else "DIFFERS",
               "overall_ranking": overall, "queries_run": len(per_case),
               "identical": identical, "mismatch": mismatch, "per_case": per_case}
    Path(args.output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "per_case"}, indent=2), flush=True)


if __name__ == "__main__":
    main()
