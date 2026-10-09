"""Final manuscript validation for submission/research_paper.tex and its compiled PDF.

Checks (1) page count, (2) that reported numbers match the frozen artifacts,
(3) that the verified corrections from docs/RQ1_FINAL_ADJUDICATION.md are present,
(4) that known stale claims are absent, and (5) citation numbering order.
Run from the repository root: python validate_final.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

TEX = Path("submission/research_paper.tex")
PDF = Path("submission/research_paper.pdf")

tex = TEX.read_text(encoding="utf-8")
body = tex[: tex.index(chr(92) + "begin{thebibliography}")]


def page_count(path: Path) -> int:
    try:
        import pypdf
        return len(pypdf.PdfReader(str(path)).pages)
    except ImportError:
        import pymupdf
        return pymupdf.open(str(path)).page_count


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


# Frozen artifacts (read-only)
control = load("artifacts/week11_initial_evaluation.json")
final = load("artifacts/week11_temporal_prerank_evaluation.json")
e3e4 = load("artifacts/e3_e4_evidence_augmented_evaluation.json")
c_cases, f_cases = control["per_case_records"], final["per_case_records"]
count = lambda rows, key: sum(bool(r[key]) for r in rows)
ctrl_sel, ctrl_100 = count(c_cases, "expected_authority_selected"), count(c_cases, "expected_authority_retrieved_at_100")
fin_sel, fin_100 = count(f_cases, "expected_authority_selected"), count(f_cases, "expected_authority_retrieved_at_100")
gained_100 = sorted(r["query_case_id"] for r in f_cases if r["expected_authority_retrieved_at_100"]
                    and not next(c for c in c_cases if c["query_case_id"] == r["query_case_id"])["expected_authority_retrieved_at_100"])
e3m = final["E3_retrieval_and_controlled_grounding_answer_key_subset"]
den = e3m["denominators"]


def freeze_counts() -> tuple[int, int, int, int]:
    """Classify each hashed freeze path: byte-identical / line-ending-only / content differs."""
    paths: dict[str, str] = {}

    def walk(o):
        if isinstance(o, dict):
            if "path" in o and "sha256" in o:
                paths[o["path"]] = o["sha256"]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(load("config/reproducibility_freeze.json"))
    exact = eol = diff = 0
    for p, h in paths.items():
        b = Path(p).read_bytes()
        if hashlib.sha256(b).hexdigest() == h:
            exact += 1
        elif h in (hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest(),
                   hashlib.sha256(re.sub(rb"(?<!\r)\n", b"\r\n", b)).hexdigest()):
            eol += 1
        else:
            diff += 1
    return len(paths), exact, eol, diff


def citation_order_ok() -> bool:
    items = re.findall(r"\\bibitem\{", tex)
    first = []
    for m in re.finditer(r"\[(\d+)\](?:--\[(\d+)\])?", body):
        for n in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
            if n not in first:
                first.append(n)
    return first == list(range(1, len(items) + 1))


n_paths, n_exact, n_eol, n_diff = freeze_counts()
fz = (f"Of the {n_paths} paths hashed in the freeze record, {n_exact} are byte-identical, {n_eol} differ only in "
      f"line endings, and {n_diff} record files without reported metrics (the dataset manifest and a development "
      f"regression log) differ in content")

checks = {
    # Numbers recomputed from frozen artifacts
    "RQ1 control R@5 (selected) matches artifact (11/30)": ctrl_sel == 11 and "0.3667 (11/30)" in tex,
    "RQ1 pre-ranking R@5 matches artifact (12/30)": fin_sel == 12 and "0.4000 (12/30) & 0.5000 (15/30)" in tex,
    "RQ1 R@100 matches artifacts (12/30 -> 15/30)": (ctrl_100, fin_100) == (12, 15) and "0.4000 (12/30)" in tex,
    "Top-100 gains named exactly as artifacts": gained_100 == ["1981_187", "1981_55", "1985_40"]
        and "1981\\_187, 1981\\_55, and 1985\\_40" in tex,
    "Integrity denominators (150 displayed, 0 violations)": den["selected_evidence_items"] == 150
        and e3m["temporal_violation_rate"] == 0 and "150/150 passed" in tex and "0 of 150" in tex,
    "Authority P/R/F1 (0.08/0.40/0.133)": round(e3m["authority_consistent_precision"], 2) == 0.08
        and "precision was 0.08, with recall 0.40 and F1 0.133" in tex,
    "Freeze sentence matches recomputed audit": fz in tex,
    "Frozen outcome metrics present": all(s in tex for s in ["0.61344", "0.612342", "0.596806", "0.592358", "0.6015",
                                                             "0.5937", "0.653402", "0.666667", "0.603175", "0.5017", "0.3341"]),
    "Frozen error-analysis counts present": all(s in tex for s in ["684", "368", "238", "213", "21/30 to 20/30", "p = 0.258"]),
    "Buckets and ranks present": "1980\\_133 at rank 15, 1981\\_55 at rank 28, 1985\\_40 at rank 78" in tex,
    "138/150 present": "138 of 150" in tex,
    # Verified corrections present
    "RQ1 reframed as characterization": "how much retrieval capacity do later and same-year judgments occupy" in tex,
    "Exploratory status stated": "so the RQ1 analysis is exploratory" in tex,
    "Control described as post-ranking filter": "post-ranking eligibility filter" in tex and "Post-ranking eligibility filter" in tex,
    "Monotonicity disclosed": "The direction of this change is constrained by the implementation" in tex,
    "Not a causal test": "it is not a causal test of retrieval quality" in tex,
    "1,979 displaced candidates": "1,979 of the 2,743" in tex,
    "Development history corrected": "Pre-ranking was adopted after comparing both conditions on Base-30" in tex,
    "1980_105 corrected": "1980\\_105 was displayed in both conditions; pre-ranking moved its raw rank from 42 to 1" in tex,
    "Year-level rule stricter than date-level": "stricter year-level rule rather than a date-level one" in tex,
    "Extract-only, no generation": "no generation component was built or evaluated" in tex,
    "H2 not tested": "the broader H2 comparison was not tested" in tex,
    "Tamper probes 90/90 scoped": "rejected all 90 altered-output probes" in tex and "not a separate retrieval evaluation" in tex,
    "Leakage finding with definition range": "14--19 cases, depending on the token definition" in tex and "12/19 versus 3/11" in tex,
    "E1/E2 training-data difference": "6,003 documents" in tex and "5,020 eligible training documents" in tex,
    "Test-count statement": "All 81 unit tests passed: 75 on the host and the six requiring PyTorch/Transformers in the project's Docker image" in tex,
    "Extension-7 reported without confirmation claim": "has no control arm and does not confirm the temporal comparison" in tex,
    # Stale claims absent
    "No stale claims": re.search(r"(?<!\d)5/30", tex) is None and not any(s in tex for s in [
        "0.1667", "net 7", "nfiltered BM25", "no temporal eligibility predicate", "held-out test split",
        "passes 81 tests", "30 manifest entries", "22 byte-exact", "primary hurdle", "top-five hit",
        "Does applying temporal eligibility", "TaxFlow", "None address", "We build on retrieval-augmented generation"]),
    "No 'held-out' except the RQ1 negation": tex.count("held-out") == 1 and "not an independent held-out test for RQ1" in tex,
    # Structure
    "Citations numbered in first-use order": citation_order_ok(),
    "Six pages": page_count(PDF) == 6,
}

failed = [k for k, v in checks.items() if not v]
for k, v in checks.items():
    print(f"[{'PASS' if v else 'FAIL'}] {k}")
print(f"\nFreeze audit recomputed: {n_paths} paths = {n_exact} identical / {n_eol} line-ending-only / {n_diff} content")
print(f"{len(checks) - len(failed)}/{len(checks)} checks passed")
sys.exit(1 if failed else 0)
