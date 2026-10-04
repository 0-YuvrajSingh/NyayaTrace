"""BM25 ranking probe: compare top-100 retrieval results between frozen and rebuilt SQLite."""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def query_top100(db_path: str, query_text: str) -> list[str]:
    """Return ordered list of top-100 chunk_ids for a BM25 query."""
    escaped = query_text.replace('"', '""')
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        rows = con.execute(
            'SELECT chunk_id FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts) LIMIT 100',
            (escaped,)
        ).fetchall()
    finally:
        con.close()
    return [r[0] for r in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frozen-db",  required=True)
    parser.add_argument("--rebuilt-db", required=True)
    parser.add_argument("--answer-key", required=True)
    parser.add_argument("--output",     required=True)
    args = parser.parse_args()

    answer_key = json.loads(Path(args.answer_key).read_text(encoding="utf-8"))
    cases = answer_key if isinstance(answer_key, list) else answer_key.get("cases", [])

    results = []
    identical = 0
    minor_drift = 0
    mismatch = 0

    for case in cases:
        case_id = case.get("case_id", case.get("id", "UNKNOWN"))
        # Use query_text if available, otherwise fall back to facts
        query_text = case.get("query_text") or case.get("facts_text") or case.get("facts", "")
        if not query_text:
            results.append({"case_id": case_id, "verdict": "SKIPPED", "reason": "no query_text"})
            continue

        try:
            frozen_top100  = query_top100(args.frozen_db,  query_text)
            rebuilt_top100 = query_top100(args.rebuilt_db, query_text)
        except Exception as e:
            results.append({"case_id": case_id, "verdict": "ERROR", "reason": str(e)})
            continue

        if frozen_top100 == rebuilt_top100:
            verdict = "MATCH"
            identical += 1
        elif set(frozen_top100) == set(rebuilt_top100):
            verdict = "MINOR_DRIFT"
            minor_drift += 1
        else:
            verdict = "MISMATCH"
            mismatch += 1
            
        results.append({
            "case_id": case_id,
            "verdict": verdict,
            "frozen_top5":  frozen_top100[:5],
            "rebuilt_top5": rebuilt_top100[:5],
        })

    overall = "MATCH" if mismatch == 0 and minor_drift == 0 else (
        "MINOR_DRIFT" if mismatch == 0 else "MISMATCH"
    )
    summary = {
        "overall": overall,
        "queries_run": len(results),
        "identical": identical,
        "minor_drift": minor_drift,
        "mismatch": mismatch,
        "per_case": results,
    }
    Path(args.output).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "per_case"}, indent=2))


if __name__ == "__main__":
    main()
