"""6-page compression batch 2: method/results/discussion (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""E1 and E2 share facts-only extraction (\\texttt{ildc-predecision-facts-v1}): text preceding a dispositive cue
and 60\\% of the document. Cases below 10\\% retention or 100 words are excluded;
selection uses
validation only, with one held-out test evaluation.""",
"""E1 and E2 share facts-only extraction (\\texttt{ildc-predecision-facts-v1}, pre-dispositive-cue text
capped at 60\\%): cases below 10\\% retention or 100 words are excluded;
validation-only selection, one held-out test evaluation."""),
("""E1 uses lowercased TF--IDF unigrams/bigrams (sublinear TF, min DF two, $L_2$,
100{,}000 features). Of
$C \\in \\{0.1, 1.0, 10.0\\}$, validation accuracy selected $C = 10.0$ (smaller $C$
ties); refit once on eligible
training plus validation and evaluated once on test. Seed 202605.""",
"""E1 is lowercased TF--IDF unigrams/bigrams (sublinear TF, min DF two, $L_2$,
100{,}000 features); validation selected $C = 10.0$ from
$C \\in \\{0.1, 1.0, 10.0\\}$ (ties to smaller $C$), refit once on train plus validation.
Seed 202605."""),
("""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}) with a new two-label head over overlapping 512-token windows with 50-token overlap.
Training uses three epochs, seed 202607, learning rate $2\\times10^{-5}$, weight
decay 0.01, warm-up ratio 0.1, and gradient
accumulation.""",
"""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}, new two-label head) over overlapping 512-token windows (50-token overlap):
three epochs, seed 202607, learning rate $2\\times10^{-5}$, weight
decay 0.01, warm-up ratio 0.1, gradient
accumulation."""),
("""Mean pooling of window logits before softmax is the primary rule, and checkpoint
selection uses validation document-level mean-logit accuracy only (majority vote
is a secondary comparison, not a selection rule). All
1{,}503 eligible test documents and 9{,}576 test windows are covered.""",
"""Mean-logit pooling is primary; checkpoint selection uses validation mean-logit
accuracy only (majority vote is secondary). All
1{,}503 test documents and 9{,}576 windows are covered."""),
("""The query builder (\\texttt{tfidf-segment-salient-terms-v1}) emits at most 32 salient
terms for a SQLite FTS5 BM25 index backed by PostgreSQL provenance.""",
"""The query builder (\\texttt{tfidf-segment-salient-terms-v1}) emits at most 32
terms for SQLite FTS5 BM25 backed by PostgreSQL provenance."""),
("""The frozen configuration (\\texttt{week11-bm25-salient-terms-preranked-temporal-v3}) admits only judgments with decision year strictly earlier than the
query year into the candidate relation \\emph{before} BM25 ordering and the
top-100 cutoff, so the full depth is spent on eligible material.""",
"""The frozen configuration (\\texttt{week11-bm25-salient-terms-preranked-temporal-v3}) admits only strictly-earlier
decision years into the candidate relation \\emph{before} BM25 ordering and the
top-100 cutoff."""),
("""Outcome prediction was subsequently added to E3 and E4 by reusing the frozen E2
checkpoint without fine-tuning: the frozen
facts extract plus the selected verbatim evidence in selection order pass through
the same 512-token/50-overlap windows with mean-logit \\texttt{argmax} (seed
202607; configuration
\\texttt{e3e4-\\allowbreak evidence-\\allowbreak augmented-\\allowbreak inlegalbert-\\allowbreak checkpoint6318-\\allowbreak v1}).
Gold labels, scores, dates, and provenance are excluded from model input.""",
"""E3/E4 outcome prediction reuses the frozen E2
checkpoint without fine-tuning: facts plus selected evidence pass through
512-token/50-overlap windows with mean-logit \\texttt{argmax} (seed
202607). Gold labels, scores, dates, and provenance are excluded."""),
("""We note the caveat plainly: the checkpoint was trained on
facts-only inputs, so applying it to facts plus retrieved passages is an
inference-time distribution shift, not evidence-aware fine-tuning. These
predictions are reported descriptively on the frozen 30-case
base and the combined 37 cases, and are
not directly comparable with the 1{,}503-case baselines.""",
"""Caveat: the checkpoint trained on
facts-only inputs, so facts-plus-passages inference is a
distribution shift, not evidence-aware fine-tuning; these
predictions are descriptive only and
not comparable with the 1{,}503-case baselines."""),
("""On the 1{,}503-case population (Table~\\ref{tab:outcome}), sparse E1 reached accuracy 0.61344 and macro-F1 0.612342,
exceeding corrected E2 mean-logit pooling at 0.596806 and 0.592358 (majority vote
0.6015 and 0.5937). All primary models exceeded
the 0.5017 majority-class accuracy.""",
"""On 1{,}503 cases (Table~\\ref{tab:outcome}), E1 reached 0.61344 accuracy and 0.612342 macro-F1,
exceeding E2 mean-logit pooling at 0.596806 and 0.592358 (majority vote
0.6015/0.5937), all above
the 0.5017 majority baseline."""),
("""On the separate 30-case subset, E3 and E4 both
reached accuracy 0.666667 and macro-F1 0.603175, with identical confusion matrices.
On the combined 37 the same predictor reaches 0.648649 and
0.607347 with confusion matrix [[6,3],[10,18]], again identical for E3
and E4 (Table~\\ref{tab:rq1strata}).
\\textbf{The equality is expected:} with no evidence rejected, the predictor received an identical
input.""",
"""On 30 cases, E3 and E4 both
reached 0.666667 accuracy and 0.603175 macro-F1 with identical confusion matrices;
on 37 cases 0.648649 and
0.607347 with [[6,3],[10,18]], again identical (Table~\\ref{tab:rq1strata}):
with no evidence rejected, the predictor saw identical
input."""),
("""The principal RQ1 result uses the combined 37-case population
(Table~\\ref{tab:rq1strata}). The seven extension cases contribute no
additional top-5 recovery (0/7) but five further top-100 recoveries at ranks
14, 16, 26, 32, and 89, with two absent; their displayed citations are
likewise fully verified (35/35). The combined figures are Recall@5
12/37 $=$ 0.324324 and Recall@100 20/37 $=$ 0.540541 over 185 displayed
citations. The lower combined Recall@5 describes the added stratum, not the base configuration.""",
"""The seven extension cases add no
top-5 recovery (0/7) but five top-100 recoveries (ranks
14, 16, 26, 32, 89; 35/35 verified). Combined: Recall@5
12/37 $=$ 0.324324, Recall@100 20/37 $=$ 0.540541 (Table~\\ref{tab:rq1strata})."""),
("""\\caption{Outcome prediction (distinct populations; not a leaderboard).}""",
"""\\caption{Outcome prediction (distinct populations).}"""),
("""\\caption{RQ1 retrieval and prediction by stratum (combined row principal).}""",
"""\\caption{RQ1 retrieval and prediction by stratum.}"""),
("""\\caption{Evidence recovery and integrity, Base-30 (30
queries; 150 citations).}""",
"""\\caption{Recovery and integrity, Base-30 (30 queries; 150 citations).}"""),
("""\\caption{Expected-authority recovery ($n=37$): 12 selected, eight retrieved but unselected,
17 absent at $k{=}100$.}""",
"""\\caption{Authority recovery ($n=37$): 12 selected, 8 unselected, 17 absent.}"""),
("""\\caption{Displayed-evidence integrity ($n=37$, 185 citations): all checks passed.}""",
"""\\caption{Evidence integrity ($n=37$, 185 citations): all passed.}"""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p2: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
