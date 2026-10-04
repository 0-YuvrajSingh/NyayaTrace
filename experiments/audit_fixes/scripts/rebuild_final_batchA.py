"""Rebuild batch A: factual corrections + method/results compression + structural removals."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
# --- factual corrections (were wiped; re-apply) ---
("""metadata is excluded. Both rules trade
recall for the guarantee that no displayed authority can post-date the matter.""",
"""metadata is excluded. Both rules trade
recall so that, under the fail-closed metadata checks applied here, no
displayed authority can post-date the matter."""),
("""Critically, four cases (\\texttt{2008\\_1629}, \\texttt{1981\\_187},
\\texttt{1982\\_29}, \\texttt{1985\\_40}) retrieved \\emph{and} selected the expected
authority yet still produced an incorrect outcome prediction: correct recovery
does not mechanically imply a correct prediction.""",
"""Critically, three cases (\\texttt{2008\\_1629}, \\texttt{1981\\_187},
\\texttt{1982\\_29}) retrieved \\emph{and} selected the expected
authority yet were predicted
incorrectly, and \\texttt{1985\\_40} was retrieved but not selected yet likewise
mispredicted: recovery does not imply correct prediction."""),
("""live data nothing was rejected --- a ceiling effect of already-valid selected
evidence, not a reduction magnitude. Three positive
controls through the unchanged verifier show the gate bites:""",
"""live data nothing was rejected --- a ceiling effect of already-valid selected
evidence, not a reduction magnitude. Three recorded positive
controls through the unchanged verifier show the gate bites:"""),
("""entries: 29 byte-exact and 10 differing only in
non-scientific metadata, with all reported metrics verified identical;
per-file evidence in the repository audit). Separately, the
local demo stack is covered by 8/8 Spring Boot service tests, 6/6 FastAPI
wrapper tests, and a passing TypeScript compile plus production frontend
build; these exercise orchestration and contracts only, never the frozen
scientific results.""",
"""entries: 28 byte-exact, one line-ending-normalized, and 10 differing only in
non-scientific metadata, with all reported metrics verified identical).
The demo stack is covered by 8/8 Spring Boot service tests and 6/6 FastAPI
wrapper tests."""),
("""\\textbf{Bundled verification.} E4 checks several integrity properties together
and cannot isolate any single component's causal contribution.""",
"""\\textbf{Bundled verification.} E4 checks several integrity properties together
and cannot isolate any single component's contribution.

\\textbf{Inference numerics.} Recomputed E3/E4 mean logits show bounded GPU
fp16 variation across runs (bounded at the fourth decimal in the
independent recomputation) that changed no decision, evidence selection, or
metric; strict serialized file hashes of E3/E4 outputs therefore differ while
substantive outputs agree.

\\textbf{Retrieval-equivalence scope.} BM25 rebuild equivalence is established
at ranking level --- identical corpus, parameters, and top-100 agreement on
all 30 evaluated queries --- not as byte-identical SQLite files, and it does
not generalize beyond the evaluated query set."""),
("""be read as representative of the ILDC test set or of
Indian legal research generally --- the primary constraint on
generality.""",
"""be read as representative of the ILDC test set or of
Indian legal research generally. The shared 14-case facts-sufficiency filter likewise narrows the
prediction population to inputs with adequate pre-decision material."""),
# --- method/results compression ---
("""E4 receives the E3 answer, retrieval-run identifier, query identity and
year, and persisted corpus records. Each displayed item must exist in the
corpus, reproduce exact passage and provenance, belong to the recorded
run, avoid the query and duplicates, and pre-date the
query year; any failure rejects the citation.

Authority consistency is evaluated separately, after verification. A fully valid
citation may differ from the single expected authority without being labelled
substantively irrelevant --- a distinction we return to in
Section~\\ref{sec:ceiling}.""",
"""E4 receives the E3 answer, retrieval-run identifier, query identity and
year, and persisted corpus records. Each displayed item must exist in the
corpus, reproduce exact passage and provenance, belong to the recorded
run, avoid the query and duplicates, and pre-date the
query year; any failure rejects the citation. Authority consistency is then
evaluated separately: a fully valid citation may differ from the single
expected authority without being substantively irrelevant (Section~\\ref{sec:ceiling})."""),
("""Outcome prediction was subsequently added to E3 and E4 by reusing the frozen E2
checkpoint without fine-tuning. A shared input builder concatenates the frozen
facts extract and the selected verbatim evidence in selection order, applies the
same 512-token windows with 50-token overlap, pools window logits by their mean,
and selects the class by \\texttt{argmax}. Gold labels, scores, dates,
provenance, and boilerplate
are excluded from model input. Seed 202607; configuration
\\texttt{e3e4-\\allowbreak evidence-\\allowbreak augmented-\\allowbreak inlegalbert-\\allowbreak checkpoint6318-\\allowbreak v1}.""",
"""Outcome prediction was subsequently added to E3 and E4 by reusing the frozen E2
checkpoint without fine-tuning: the frozen
facts extract plus the selected verbatim evidence in selection order pass through
the same 512-token/50-overlap windows with mean-logit \\texttt{argmax} (seed
202607; configuration
\\texttt{e3e4-\\allowbreak evidence-\\allowbreak augmented-\\allowbreak inlegalbert-\\allowbreak checkpoint6318-\\allowbreak v1}).
Gold labels, scores, dates, and provenance are excluded from model input."""),
("""We note the methodological caveat plainly: the checkpoint was trained on
facts-only inputs, so applying it to facts plus retrieved passages is an
inference-time distribution shift, not evidence-aware fine-tuning. These
predictions are therefore reported descriptively --- on the frozen 30-case
base and, in the RQ1 extension, on the combined 37 cases --- using the frozen E2
checkpoint at inference time, and are
not directly comparable with the 1{,}503-case baselines, which form a
separate population with a different denominator.""",
"""We note the caveat plainly: the checkpoint was trained on
facts-only inputs, so applying it to facts plus retrieved passages is an
inference-time distribution shift, not evidence-aware fine-tuning. These
predictions are reported descriptively on the frozen 30-case
base and the combined 37 cases, and are
not directly comparable with the 1{,}503-case baselines."""),
("""E4 jointly checks corpus existence,
exact passage/provenance identity, run membership, duplicate
status, and temporal eligibility over shared final retrieval
and evidence. Aggregate reliability cannot be attributed to any one
component; the supported claim concerns the complete bundle.""",
"""E4 jointly checks corpus existence,
passage/provenance identity, run membership, duplicate
status, and temporal eligibility. Aggregate reliability cannot be attributed to any one
component; the supported claim concerns the complete bundle."""),
("""Each chunk is keyed by a stable identifier built from its source path and
passage
location. The persisted record stores: source ID, source
case ID where available, citation, exact decision date, court, local PDF
file, page number, character start and end, and chunk text. Retrieval runs record query ID, year,
query text, index version, temporal policy, rank, score, and temporal status.""",
"""Each chunk carries a stable identifier from its source path and
passage location, with stored source ID, case ID, citation, exact decision date, court, PDF
file, page and character bounds, and chunk text. Retrieval runs record query ID, year,
query text, index version, temporal policy, rank, score, and temporal status."""),
("""In our results, states (1)--(3) occur zero times and state (4) occurs
in 18 of 30 cases --- a profile that a single aggregate score would render
invisible.""",
"""In our results, states (1)--(3) occur zero times and state (4) occurs
in 18 of 30 cases."""),
("""This does not show domain pre-training is ineffective in general, only that the
sparse baseline performed better under these frozen settings; Section~\\ref{sec:error}
shows the two models make substantially non-identical errors.""",
"""This does not show domain pre-training is ineffective in general, only that the
sparse baseline performed better under these frozen settings."""),
("""Authority-consistency precision was 0.08, with recall 0.40 and F1 0.133 --- to
be read structurally, not as a fabrication rate:
with one credited authority per case and five displayed, perfect inclusion caps
the measure at $30/150 = 0.20$, so 0.08 is 40\\% of ceiling.""",
"""Authority-consistency precision was 0.08, with recall 0.40 and F1 0.133:
with one credited authority per case and five displayed, perfect inclusion caps
the measure at $30/150 = 0.20$, so 0.08 is 40\\% of ceiling."""),
("""The 138 non-matching displayed citations are \\emph{not} independently annotated
for substantive legal relevance and cannot be declared incorrect. They passed
every integrity check; they simply are not the one authority the key records.
Reporting this metric without its ceiling would materially misrepresent the
system.""",
"""The 138 non-matching displayed citations are \\emph{not} independently annotated
for substantive legal relevance. They passed
every integrity check; they simply are not the one authority the key records."""),
("""The final configuration came from three bounded changes, each validated on the
nine-case probe before the 30-case held-out test: full-input salient terms
took the probe from 0/9 to 3/9 at $k{=}100$; the 80\\% coverage self-match
condition took it to 6/9 and forced withdrawal of an over-broad
lexical-mismatch claim; pre-ranking temporal filtering took it to 7/9 and,
carried over, lifted Recall@5 from 5/30 to 12/30 and Recall@100 from 12/30 to
15/30 \\emph{without losing any of the 12 prior top-100 successes}.""",
"""The final configuration came from three bounded changes, each validated on the
nine-case probe before the 30-case held-out test: full-input salient terms
(0/9 to 3/9 at $k{=}100$); the 80\\% coverage self-match
condition (to 6/9); pre-ranking temporal filtering (to 7/9), which
carried over to Recall@5 5/30 to 12/30 and Recall@100 12/30 to
15/30 \\emph{without losing any of the 12 prior top-100 successes}."""),
("""Temporal capacity is not the whole story. \\texttt{2013\\_35} stayed absent
despite 79 eligible candidates in its raw top 100, while
\\texttt{1980\\_105} was recovered from only three and
became a top-five hit: pool size and lexical relevance contribute
independently, with residual lexical mismatch the prominent unresolved
cause.""",
"""Temporal capacity is not the whole story. \\texttt{2013\\_35} stayed absent
despite 79 eligible candidates in its raw top 100, while
\\texttt{1980\\_105} was recovered from only three and
became a top-five hit: residual lexical mismatch is the prominent unresolved
cause."""),
("""The analysis is read-only over final frozen outputs; reconstructed E1
and inference-only E2 predictions reproduced their metrics
before per-case joining. Across 1{,}503 cases, both models were correct on 684
and both wrong on 368; E1 alone was correct on 238 and E2 alone on 213
(Table~\\ref{tab:overlap}) --- complementary errors suggesting ensemble or
disagreement-triggered routing as future work.""",
"""The analysis is read-only over final frozen outputs. Across 1{,}503 cases, both models were correct on 684
and both wrong on 368; E1 alone was correct on 238 and E2 alone on 213
(on the 30-case key: 18/3/3/6)."""),
("""In the evidence-augmented run, E2 was wrong while E3 and E4 were correct for two
cases (\\texttt{1974\\_36}, \\texttt{1984\\_136}). E3-correct/E4-wrong and
E3-wrong/E4-correct each occurred in 0/30 cases, because verification changed
neither the selected evidence nor the shared predictor input.""",
"""In the evidence-augmented run, E2 was wrong while E3 and E4 were correct for two
cases (\\texttt{1974\\_36}, \\texttt{1984\\_136}); E3/E4 verification changed
neither the selected evidence nor the shared predictor input (0/30 divergences)."""),
("""Table~\\ref{tab:buckets} gives the exhaustive partition: the middle bucket
isolates \\emph{selection} failure (available but undisplayed, addressable by a
better selector), while the absent bucket requires upstream
improvement in representation, matching, ranking, or coverage.""",
"""The exhaustive partition is: 12 retrieved and
selected; 3 retrieved but unselected
(\\texttt{1980\\_133} rank 15, \\texttt{1981\\_55} rank 28,
\\texttt{1985\\_40} rank 78); and 15 absent at $k{=}100$.
The middle bucket isolates \\emph{selection} failure (available but undisplayed), while the absent bucket requires upstream
improvement."""),
]

fails = 0
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        print(f"EDIT {i}: found {c} (expected 1)")
        fails += 1
        continue
    t = t.replace(old, new)
print(f"text edits applied: {len(EDITS) - fails}/{len(EDITS)}")
if fails:
    raise SystemExit(1)

# --- structural removals by markers ---
lines = t.split("\n")


def drop_env(start_marker, end_marker="\\end{table}"):
    global lines
    s = next(i for i, l in enumerate(lines) if start_marker in l)
    b = next(i for i in range(s, len(lines)) if lines[i].strip() == "\\begin{table}[t]")
    e = next(i for i in range(s, len(lines)) if lines[i].strip() == end_marker)
    del lines[b:e + 1]
    return b


def drop_figure(figfile):
    global lines
    s = next(i for i, l in enumerate(lines) if figfile in l)
    b = next(i for i in range(s, -1, -1) if lines[i].strip() == "\\begin{figure}[t]")
    e = next(i for i in range(s, len(lines)) if lines[i].strip() == "\\end{figure}")
    del lines[b:e + 1]


drop_env("\\caption{Outcome-error overlap")
drop_env("\\caption{Exhaustive authority-recovery partition")
drop_figure("figures/fig1_outcome.pdf")
drop_figure("figures/fig4_investigation.pdf")
drop_figure("figures/fig5_explanation.pdf")

# worked example subsection -> comment
s = next(i for i, l in enumerate(lines) if "\\subsection{Worked example" in l)
e = next(i for i in range(s, len(lines)) if "\\section{Limitations" in l)
lines[s:e] = ["% Worked-example detail retained in frozen artifacts; subsection removed for length.", ""]

t = "\n".join(lines)
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
print("structural removals done")
