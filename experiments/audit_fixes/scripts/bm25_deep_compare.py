"""Deep BM25 comparison: manifest + chunk identity + production ranking probe.

Uses the exact production temporal preranked SQL and salient TF-IDF query
construction for the frozen 30-case evaluation subset.
No database connection required (SQLite + parquet + facts only).
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


def count_and_hash_chunk_ids(db_path: str) -> tuple[int, str, str, str]:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        n_fts = con.execute("SELECT count(*) FROM chunks_fts").fetchone()[0]
        n_meta = con.execute("SELECT count(*) FROM chunk_temporal_metadata").fetchone()[0]
        h = hashlib.sha256()
        first5: list[str] = []
        last5: list[str] = []
        # Stream ordered chunk_ids from FTS (rowid order may differ from chunk_id order;
        # use explicit ORDER BY chunk_id for canonical identity).
        # FTS5 tables support ORDER BY chunk_id? chunk_id is UNINDEXED but stored.
        # Safer: hash from temporal metadata ordered by chunk_id (same IDs).
        cur = con.execute("SELECT chunk_id FROM chunk_temporal_metadata ORDER BY chunk_id")
        n = 0
        window: list[str] = []
        for (cid,) in cur:
            h.update(cid.encode("utf-8"))
            h.update(b"\x00")
            n += 1
            window.append(cid)
            if len(window) > 5:
                window.pop(0)
            if n <= 5:
                first5.append(cid)
        last5 = window
        return n_fts, h.hexdigest(), str(first5), str(last5)
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

    # 1. Chunk identity
    f_n, f_hash, f_first, f_last = count_and_hash_chunk_ids(args.frozen_db)
    r_n, r_hash, r_first, r_last = count_and_hash_chunk_ids(args.rebuilt_db)
    print(f"frozen fts count: {f_n} hash: {f_hash}")
    print(f"rebuilt fts count: {r_n} hash: {r_hash}")
    print(f"chunk_id identity: {'IDENTICAL' if (f_n == r_n and f_hash == r_hash) else 'DIFFERS'}")

    # 2. Production ranking probe over 30 eval cases
    answer_key = json.loads(Path(args.answer_key).read_text(encoding="utf-8"))
    entries = [e for e in answer_key["entries"] if e.get("status") == "evaluation"]
    print(f"eval entries: {len(entries)}")
    table = pq.read_table(args.test_split, columns=["id", "text"])
    text_by_id = {str(r["id"]): str(r["text"] or "") for r in table.to_pylist()}
    rule = load_facts_extraction_rule(Path(args.facts_config))

    identical = 0
    mismatch = 0
    per_case = []
    for e in sorted(entries, key=lambda x: str(x["query_case_id"])):
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
        per_case.append({
            "query_case_id": cid,
            "query_year": year,
            "verdict": verdict,
            "frozen_top5": f_top[:5],
            "rebuilt_top5": r_top[:5],
            "frozen_n": len(f_top),
            "rebuilt_n": len(r_top),
        })
        print(f"{cid} year={year} -> {verdict} (n={len(f_top)}/{len(r_top)})")

    overall = "MATCH" if mismatch == 0 else "MISMATCH"
    summary = {
        "frozen_fts_count": f_n,
        "rebuilt_fts_count": r_n,
        "chunk_id_ordered_sha256_frozen": f_hash,
        "chunk_id_ordered_sha256_rebuilt": r_hash,
        "chunk_identity": "IDENTICAL" if (f_n == r_n and f_hash == r_hash) else "DIFFERS",
        "overall_ranking": overall,
        "queries_run": len(per_case),
        "identical": identical,
        "mismatch": mismatch,
        "per_case": per_case,
    }
    Path(args.output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "per_case"}, indent=2))


if __name__ == "__main__":
    main()
