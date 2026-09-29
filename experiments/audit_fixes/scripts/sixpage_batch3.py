"""6-page compression batch 3: discussion/limitations/conclusion (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""The principal RQ3 evaluation is a blinded exploratory comparison
by four LLM raters over 14
paired cases on five transparency
dimensions with a forced preference. The structured presentation was preferred in 56/56 evaluations
($+$1.75 linkage,
$+$1.00 verifiability, $+$2.48 traceability, $+$2.52
clarity, $+$1.98 transparency; overall
$+$1.95, 4.66 vs.\\ 2.71).""",
"""Blinded exploratory comparison
by four LLM raters over 14
paired cases (five transparency
dimensions, forced preference): structured presentation preferred 56/56
($+$1.75 linkage,
$+$1.00 verifiability, $+$2.48 traceability, $+$2.52
clarity, $+$1.98 transparency; overall
$+$1.95, 4.66 vs.\\ 2.71)."""),
("""The analysis is read-only over final frozen outputs. Across 1{,}503 cases, both models were correct on 684
and both wrong on 368; E1 alone was correct on 238 and E2 alone on 213
(on the 30-case key: 18/3/3/6).""",
"""Read-only over frozen outputs: both models correct on 684
of 1{,}503 cases,
both wrong on 368; E1-only 238, E2-only 213
(key-30: 18/3/3/6)."""),
("""In the evidence-augmented run, E2 was wrong while E3 and E4 were correct for two
cases (\\texttt{1974\\_36}, \\texttt{1984\\_136}); E3/E4 verification changed
neither the selected evidence nor the shared predictor input (0/30 divergences).""",
"""E2 was wrong while E3/E4 were correct for
\\texttt{1974\\_36} and \\texttt{1984\\_136}; verification changed
neither evidence nor input (0/30 divergences)."""),
("""Critically, three cases (\\texttt{2008\\_1629}, \\texttt{1981\\_187},
\\texttt{1982\\_29}) retrieved \\emph{and} selected the expected
authority yet were predicted
incorrectly, and \\texttt{1985\\_40} was retrieved but not selected yet likewise
mispredicted: recovery does not imply correct prediction.""",
"""Three cases (\\texttt{2008\\_1629}, \\texttt{1981\\_187},
\\texttt{1982\\_29}) retrieved \\emph{and} selected the expected
authority yet were mispredicted;
\\texttt{1985\\_40} was retrieved but not selected yet likewise
mispredicted."""),
("""\\textbf{Scope.} English-language Indian Supreme Court judgments
only.""",
"""\\textbf{Scope.} English-language Indian Supreme Court judgments
only; no cross-jurisdictional transfer."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p3a: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
