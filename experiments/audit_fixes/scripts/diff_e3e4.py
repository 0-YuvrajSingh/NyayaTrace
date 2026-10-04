"""Field-level diff of frozen vs replayed E3/E4 (excluding retrieval_run_id)."""
import json
from pathlib import Path

ROOT = Path("/repo")
ref = json.loads((ROOT / "artifacts/e3_e4_evidence_augmented_evaluation.json").read_text())
rep = json.loads(Path("/out/e3e4_replay.json").read_text())


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k != "retrieval_run_id"}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


rs, ps = strip(ref), strip(rep)
print("top-level keys equal:", sorted(rs.keys()) == sorted(ps.keys()))
for k in sorted(set(rs) | set(ps)):
    if k == "per_case_records":
        continue
    print(f"{k}: {'IDENTICAL' if rs.get(k) == ps.get(k) else 'DIFFERS'}")

rr = {r["query_case_id"]: r for r in rs["per_case_records"]}
pr = {r["query_case_id"]: r for r in ps["per_case_records"]}
print("per-case id sets equal:", set(rr) == set(pr))
print("per-case order identical:", [r["query_case_id"] for r in rs["per_case_records"]] == [r["query_case_id"] for r in ps["per_case_records"]])

diff_cases = 0
for cid in sorted(set(rr) & set(pr)):
    a, b = rr[cid], pr[cid]
    if a != b:
        diff_cases += 1
        print(f"--- {cid} DIFFERS ---")
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                if k in ("E3", "E4"):
                    for sk in sorted(set(a.get(k, {})) | set(b.get(k, {}))):
                        if a.get(k, {}).get(sk) != b.get(k, {}).get(sk):
                            av, bv = a[k][sk], b[k][sk]
                            if isinstance(av, list) and isinstance(bv, list) and len(av) == len(bv):
                                for i, (x, y) in enumerate(zip(av, bv)):
                                    if x != y:
                                        print(f"  {k}.{sk}[{i}] differs:")
                                        if isinstance(x, dict) and isinstance(y, dict):
                                            for fk in sorted(set(x) | set(y)):
                                                if x.get(fk) != y.get(fk):
                                                    print(f"    field {fk!r}: ref={repr(x.get(fk))[:200]} replay={repr(y.get(fk))[:200]}")
                                        else:
                                            print(f"    ref={repr(x)[:300]}")
                                            print(f"    replay={repr(y)[:300]}")
                                        if i >= 2:
                                            print("    ... (truncated)")
                                            break
                            else:
                                print(f"  {k}.{sk}: ref={repr(av)[:300]} replay={repr(bv)[:300]}")
                else:
                    print(f"  {k}: ref={repr(a.get(k))[:200]} replay={repr(b.get(k))[:200]}")
        if diff_cases >= 3:
            print("... (truncated after 3 cases)")
            break
print(f"cases differing: {diff_cases}/30")
# Recall counts from raw per-case flags
for name, recs in (("ref", rs["per_case_records"]), ("replay", ps["per_case_records"])):
    at5 = sum(1 for r in recs if r["expected_authority_retrieved_at_5"])
    at100 = sum(1 for r in recs if r["expected_authority_retrieved_at_100"])
    sel = sum(1 for r in recs if r["expected_authority_selected"])
    print(f"{name}: at5={at5}/30 at100={at100}/30 selected={sel}/30")
