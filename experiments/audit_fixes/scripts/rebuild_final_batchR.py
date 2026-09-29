"""Final restructure batch R: Base-30 core, artifact relegation (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
# 1. Abstract: reframe findings around 1503 + Base-30
("""We report three findings on combined 37 cases
(frozen 30 plus 7 extension, in strata). First, naive ILDC--eCourts identifier matching is unsafe:
11 of 5{,}391 syntactic matches survived alignment.
Second, pre-ranking temporal eligibility
raised Recall@5 from
5/30 to 12/30 and Recall@100 from 12/30 to 15/30 on the frozen base (12/37
and 20/37 combined). Third, all 185 displayed citations passed verification,
with zero unsupported claims,
while 17 remained
absent at $k{=}100$. Exploratory 14-case LLM-rater
comparison: structured presentation preferred 56/56 (presentation
evidence only).""",
"""We report three independently replayed findings. First, naive ILDC--eCourts identifier matching is unsafe:
11 of 5{,}391 syntactic matches survived alignment.
Second, pre-ranking temporal eligibility
raised Recall@5 from
5/30 to 12/30 and Recall@100 from 12/30 to 15/30 on the frozen 30-case base.
Third, all 150 displayed base citations passed verification,
with zero unsupported claims,
while 15 expected authorities remained
absent at $k{=}100$. Outcome baselines on 1{,}503 cases use their own population.
A separate 14-case LLM-based presentation comparison was recorded as exploratory
evidence only."""),
# 2. Intro central finding -> Base-30
("""The central finding is a dissociation: all 185 displayed citations
cleared verification with no
unsupported claim, yet 17 of 37
expected authorities never appeared in the top 100.""",
"""The central finding is a dissociation: all 150 displayed base citations
cleared verification with no
unsupported claim, yet 15 of 30
expected authorities never appeared in the top 100."""),
# 3. Scope populations: name replay boundary
("""populations (1{,}503 outcome cases, 30 frozen plus 7 additive
evidence cases, paired explanation examples).""",
"""populations (1{,}503 outcome cases; 30 frozen evidence cases as the replayed core;
7 additive extension cases and paired explanation examples reported as artifacts)."""),
# 4. Combined RQ1 prose -> relegate extension, keep base principal
("""The principal RQ1 result uses the combined 37-case population
(Table~\\ref{tab:rq1strata}). The seven extension cases contribute no
additional top-5 recovery (0/7) but five further top-100 recoveries at ranks
14, 16, 26, 32, and 89, with two absent; their displayed citations are
likewise fully verified (35/35). The combined figures are Recall@5
12/37 $=$ 0.324324 and Recall@100 20/37 $=$ 0.540541 over 185 displayed
citations. The lower combined Recall@5 describes the added stratum, not the base configuration.""",
"""The principal RQ1 result is the Base-30 row of Table~\\ref{tab:rq1strata}.
The Extension-7 stratum (0/7 top-5; five top-100 recoveries; 35/35 verified)
and the Combined-37 row are reported from frozen artifacts and were not
independently replayed."""),
# 5. Table III caption qualifier
("""\\caption{RQ1 retrieval and prediction by stratum (combined row principal).}""",
"""\\caption{RQ1 retrieval and prediction by stratum (Base-30 replayed; extension rows reported, not replayed).}"""),
# 6. Central result -> Base-30
("""\\textbf{This is the paper's central result.} The system verified everything it displayed (185/185
combined; 150/150 base) while recovering the expected authority
in 20 of 37 cases at $k{=}100$ (15/30 base).""",
"""\\textbf{This is the paper's central result.} The system verified everything it displayed (150/150)
while recovering the expected authority
in 15 of 30 cases at $k{=}100$."""),
# 7. Positive controls -> remove sentence
("""E4 verification is fail-closed: any failing check rejects the citation. On
live data nothing was rejected, a ceiling effect of already-valid evidence. Recorded positive
controls (altered, fabricated, and backdated cases, 37/37 each) show the gate bites.""",
"""E4 verification is fail-closed: any failing check rejects the citation. On
live data nothing was rejected, a ceiling effect of already-valid evidence."""),
# 8. Figures 2-3 (combined data) -> remove; tables carry verified base
# (handled structurally below)
# 9. Probe pathway -> artifact label
("""The final configuration came from three bounded changes, each validated on the
nine-case probe before the 30-case held-out test: full-input salient terms
(0/9 to 3/9 at $k{=}100$); the 80\\% coverage self-match
condition (to 6/9); pre-ranking temporal filtering (to 7/9), which
carried over to Recall@5 5/30 to 12/30 and Recall@100 12/30 to
15/30 \\emph{without losing any of the 12 prior top-100 successes}.""",
"""The final configuration came from three recorded development steps on a
nine-case probe (0/9 to 3/9 to 6/9 to 7/9 at $k{=}100$); pre-ranking temporal filtering,
carried to the held-out base, moved Recall@5 5/30 to 12/30 and Recall@100 12/30 to
15/30 \\emph{without losing any of the 12 prior top-100 successes}. Probe history is
reported from development records, not replayed."""),
# 10. LLM section -> non-numeric exploratory
("""The principal RQ3 evaluation is a blinded exploratory comparison
by four LLM raters over 14
paired cases on five transparency
dimensions with a forced preference. The structured presentation was preferred in 56/56 evaluations
($+$1.75 linkage,
$+$1.00 verifiability, $+$2.48 traceability, $+$2.52
clarity, $+$1.98 transparency; overall
$+$1.95, 4.66 vs.\\ 2.71).

This is explicitly \\emph{not} human evaluation: no significance test was run, and nothing about human preference or legal correctness follows.
Two raters produced byte-identical
vectors, retained separately;
the seven-case self-review (7/7) is formative,
non-independent evidence superseded above.""",
"""A separate 14-case LLM-based presentation comparison was recorded as exploratory
evidence and is not treated as independently reproduced or as evidence of human
preference. No significance test was run; the seven-case self-review beneath it is
formative, non-independent evidence."""),
# 11. Conclusion -> Base-30
("""The principal finding is a dissociation. Every one of 185 displayed citations
passed verification, with zero unsupported claims,
while 17 of
the 37 expected authorities were
absent at $k{=}100$.""",
"""The principal finding is a dissociation. Every one of 150 displayed base citations
passed verification, with zero unsupported claims,
while 15 of
the 30 expected authorities were
absent at $k{=}100$."""),
("""The supporting results are reported with their limits. The sparse TF--IDF baseline outperformed corrected InLegalBERT
under the frozen settings (1{,}503 cases). Inference-time evidence augmentation
reached 0.666667 accuracy and 0.603175 macro-F1 on the frozen 30-case subset
(0.648649 and 0.607347 on the combined 37), descriptively and under acknowledged
distribution shift. Presentation evidence is exploratory, not human preference.""",
"""The supporting results are reported with their limits. The sparse TF--IDF baseline outperformed corrected InLegalBERT
under the frozen settings (1{,}503 cases). Inference-time evidence augmentation
reached 0.666667 accuracy and 0.603175 macro-F1 on the frozen 30-case subset,
descriptively and under acknowledged distribution shift."""),
# 12. Reproducibility scope
("""checks (14/14 documentation; freeze audit of 39 entries:
28 byte-exact, one line-ending-normalized, 10 metadata-differing; all reported
metrics verified identical).""",
"""checks (14/14 documentation; freeze audit of 39 entries:
28 byte-exact, one line-ending-normalized, 10 metadata-differing).
All independently replayed primary metrics matched their frozen references; E3/E4
decisions, evidence selections, and metrics matched despite bounded fp16 variation,
and BM25 matched at ranking level on the 30 evaluated queries."""),
# 13. Limitations: extension replay boundary
("""\\textbf{Answer-key size and era concentration.} Evidence evaluation rests on
30 frozen cases, extended additively to 37;""",
"""\\textbf{Answer-key size and era concentration.} Evidence evaluation rests on
30 frozen replayed cases, extended additively to 37 (extension reported, not replayed);"""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("R: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))

lines = t.split("\n")


def drop_figure(figfile):
    s = next(i for i, l in enumerate(lines) if figfile in l)
    b = next(i for i in range(s, -1, -1) if lines[i].strip() == "\\begin{figure}[t]")
    e = next(i for i in range(s, len(lines)) if lines[i].strip() == "\\end{figure}")
    del lines[b:e + 1]


drop_figure("figures/fig2_funnel.pdf")
drop_figure("figures/fig3_integrity.pdf")

t = "\n".join(lines)
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
print("restructure done")
