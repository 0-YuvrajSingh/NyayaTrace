"""Rebuild batch D: compression edits (non-aborting; reports mismatches)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
("defects, making citation verifiability a functional requirement. We present an",
 "defects. We present an"),
("""temporally eligible, provenance-bound, and mechanically verifiable. The design is extractive: material propositions
are shown verbatim with locators, and outcome prediction is
kept separate so a classification score can never stand in for
evidence quality. We report three findings on a combined 37-case""",
"""temporally eligible, provenance-bound, and mechanically verifiable, with outcome
prediction kept separate. We report three findings on a combined 37-case"""),
("""7-case extension, analysed in strata). First, naive identifier matching between ILDC and an eCourts-derived
judgment archive is unsafe: of 5{,}391 syntactic matches only 11
survived content alignment, motivating a reusable gate.""",
"""7-case extension, analysed in strata). First, naive identifier matching between ILDC and an eCourts-derived
judgment archive is unsafe: of 5{,}391 syntactic matches only 11
survived alignment."""),
("""Second, pre-ranking temporal eligibility with salient-term queries and a
self-match guard raised Recall@5 from""",
"""Second, pre-ranking temporal eligibility
raised Recall@5 from"""),
("""temporal verification, with zero unsupported claims across the 37 cases,
while 17 expected authorities remained
absent at $k{=}100$: verification and retrieval must be measured
on separate denominators. Outcome baselines on 1{,}503 ILDC
cases and inference-time evidence augmentation are reported with
their own populations and limits. A blinded 14-case, four-LLM-rater""",
"""temporal verification, with zero unsupported claims,
while 17 expected authorities remained
absent at $k{=}100$. A blinded 14-case, four-LLM-rater"""),
("""produce evidence a reviewer can
locate, inspect, and independently verify.""",
"""produce evidence a reviewer can verify."""),
("""these failures are frequent rather than exceptional \\cite{dahl2024}, and related
work has probed how far explicit legal standards can be communicated to language
models at all \\cite{nay2023}.""",
"""these failures are frequent rather than exceptional \\cite{dahl2024}, and how far explicit legal standards can be communicated to models remains open \\cite{nay2023}."""),
("""The central empirical observation is a dissociation that a single aggregate
score would erase. Under the final configuration, all 185 displayed citations
across the combined 37 cases
cleared grounding, provenance, duplicate, and temporal checks, with no
unsupported claim among the 37 cases; at the same time, 17 of the 37 independently
verified expected authorities never appeared among the top 100 candidates
returned by the retriever. Correctness of what is shown and completeness of
what is found are therefore separate properties. Reporting only a combined
``citation correctness'' figure would hide
exactly the gap a reader needs in order to decide how much to trust the
output.""",
"""The central empirical observation is a dissociation. All 185 displayed citations
cleared grounding, provenance, duplicate, and temporal checks, with no
unsupported claim; at the same time, 17 of 37
verified expected authorities never appeared in the top 100."""),
("""\\item \\textbf{A quantified cross-corpus identity failure and its remedy.}
Converting eCourts identifiers of the form""",
"""\\item \\textbf{A quantified cross-corpus identity failure and its remedy.}
\\texttt{YYYY INSC N} to"""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print(f"D1: {len(EDITS) - len(fails)}/{len(EDITS)}, fails: {fails}")
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
