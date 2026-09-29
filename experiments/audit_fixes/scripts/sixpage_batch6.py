"""6-page compression batch 6 (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""Second, pre-ranking temporal eligibility
raised Recall@5 from
5/30 to 12/30 and Recall@100 from 12/30 to 15/30 (12/37
and 20/37 combined). Third, all 185 displayed citations passed verification,
with zero unsupported claims,
while 17 remained
absent at $k{=}100$. Exploratory 14-case LLM-rater
comparison: structured presentation preferred 56/56 (presentation
evidence only).""",
"""Second, pre-ranked temporal eligibility:
Recall@5 5/30 to 12/30, Recall@100 12/30 to 15/30 (12/37
and 20/37 combined). Third, all 185 citations verified,
zero unsupported,
17 absent
at $k{=}100$. Exploratory 14-case LLM comparison: structured preferred 56/56."""),
("""The central finding is a dissociation: all 185 displayed citations
cleared verification with no
unsupported claim, yet 17 of 37
expected authorities never appeared in the top 100.""",
"""Central dissociation: 185 displayed citations
verified, zero unsupported,
yet 17 of 37
expected authorities absent from the top 100."""),
("""\\item \\textbf{Cross-corpus identity failure, quantified and remedied.}
\\texttt{YYYY INSC N} to \\texttt{YYYY\\_N} conversion: 5{,}391 syntactic candidates, 11
passing content alignment (Section~\\ref{sec:alignment}).""",
"""\\item \\textbf{Identity failure, quantified and remedied.}
\\texttt{YYYY INSC N} to \\texttt{YYYY\\_N}: 5{,}391 candidates, 11
passing alignment (Section~\\ref{sec:alignment})."""),
("""\\item \\textbf{Pre-ranking temporal eligibility.} Availability as a predicate
inside BM25 retrieval (Section~\\ref{sec:e3}): Recall@5
5/30 to 12/30 with no regressions.""",
"""\\item \\textbf{Pre-ranking eligibility.} Availability inside BM25
(Section~\\ref{sec:e3}): Recall@5
5/30 to 12/30, no regressions."""),
("""On 30 cases, E3 and E4 both
reached 0.666667 accuracy and 0.603175 macro-F1 with identical confusion matrices;
on 37 cases 0.648649 and
0.607347 with [[6,3],[10,18]], again identical (Table~\\ref{tab:rq1strata}):
with no evidence rejected, the predictor saw identical
input.""",
"""On 30 cases, E3/E4 reached 0.666667/0.603175 with identical confusion matrices;
on 37 cases 0.648649/
0.607347 with [[6,3],[10,18]] (Table~\\ref{tab:rq1strata}):
no rejected evidence, identical
input."""),
("""The seven extension cases add no
top-5 recovery (0/7) but five top-100 recoveries (ranks
14, 16, 26, 32, 89; 35/35 verified). Combined: Recall@5
12/37 $=$ 0.324324, Recall@100 20/37 $=$ 0.540541 (Table~\\ref{tab:rq1strata}).""",
"""Extension-7 adds no
top-5 recovery (0/7) but five top-100 recoveries (ranks
14, 16, 26, 32, 89; 35/35 verified). Combined: R@5
12/37, R@100 20/37 (Table~\\ref{tab:rq1strata})."""),
("""Principal finding: all 185 displayed citations
passed verification with zero unsupported claims,
while 17 of
37 expected authorities were
absent at $k{=}100$.""",
"""Principal finding: 185 citations
verified, zero unsupported,
while 17 of
37 authorities were
absent at $k{=}100$."""),
("""Supporting results, with limits: sparse TF--IDF beat corrected InLegalBERT
(1{,}503 cases). Evidence augmentation
reached 0.666667/0.603175 on 30 cases
(0.648649/0.607347 on 37), descriptive only, under
distribution shift. Presentation evidence is exploratory, not human preference.""",
"""Supporting results, with limits: TF--IDF beat InLegalBERT
(1{,}503). Augmentation
reached 0.666667/0.603175 (30 cases),
0.648649/0.607347 (37 cases), descriptive only."""),
("""\\textbf{Future work.} Era-balanced key (75--100); blinded independent review;
hybrid retrieval; evidence-sensitive uncertainty language.""",
"""\\textbf{Future work.} Era-balanced key; blinded review;
hybrid retrieval; uncertainty language."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p6: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
