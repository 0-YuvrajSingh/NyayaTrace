"""6-page compression batch 5: final cuts (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""Fluent legal output conceals failures: nonexistent authorities, misattributed
passages, post-dated or unretrieved matter. A 2026 Supreme Court of India
ruling (2026 INSC 668) overturned tribunal findings built on exactly these
defects.""",
"""Fluent legal output conceals failed citations: nonexistent authorities,
misattributed passages, post-dated matter. A 2026 Supreme Court of India
ruling (2026 INSC 668) overturned tribunal findings on exactly these
defects."""),
("""We therefore require: stable locators on retrieved facts, duplicate
exclusion, verbatim-only rendering,
and per-citation verification against corpus and retrieval run.""",
"""We therefore require stable locators, duplicate
exclusion, verbatim-only rendering,
and per-citation verification."""),
("""\\textbf{Scope.} No legal
correctness for retrieved authorities, no autonomous legal advisor, no
claim that retrieval improves outcome prediction: a
researcher-facing prototype on four non-pooled
populations (1{,}503 outcome cases, 30 frozen plus 7 additive
evidence cases, paired explanation examples).""",
"""\\textbf{Scope.} No legal-correctness, advisor, or retrieval-improves-prediction
claim: a
researcher-facing prototype on four non-pooled
populations (1{,}503 cases, 30 frozen plus 7
evidence cases, paired examples)."""),
("""Three questions. \\textbf{RQ1:} Does retrieved evidence improve reliability and retrieval over a facts-only
baseline (E2 versus E3; E1 for context)? \\textbf{RQ2:} Does
provenance-constrained verification reduce
unsupported claims?
\\textbf{RQ3:} Can structured presentation improve
verifiable transparency (evidence held constant)?""",
"""Three questions. \\textbf{RQ1:} Retrieved evidence versus facts-only
baseline (E2 versus E3; E1 for context)? \\textbf{RQ2:} Does
verification reduce
unsupported claims?
\\textbf{RQ3:} Does structured presentation improve
transparency (evidence held constant)?"""),
("""ILDC Single: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test); a shared sufficiency rule excluded 14 test records,
leaving 1{,}503 cases.""",
"""ILDC Single: 7{,}593 judgments (5{,}082/994/1{,}517 train/val/test); 14 excluded,
1{,}503 remain."""),
("""The eCourts-derived evidence corpus (Indian Supreme Court,
1950--2020): 39{,}069 English
PDF instances, 39{,}066 accepted, yielding
2{,}343{,}435 chunks, of which 2{,}036{,}981 unique chunks were loaded
into PostgreSQL provenance and a SQLite FTS5 BM25 index.""",
"""Evidence corpus (Indian Supreme Court,
1950--2020): 39{,}069 English
PDFs, 39{,}066 accepted, yielding
2{,}343{,}435 chunks (2{,}036{,}981 unique loaded
into PostgreSQL + SQLite FTS5 BM25)."""),
("""E1 is lowercased TF--IDF unigrams/bigrams (sublinear TF, min DF two, $L_2$,
100{,}000 features); validation selected $C = 10.0$ from
$C \\in \\{0.1, 1.0, 10.0\\}$ (ties to smaller $C$), refit once on train plus validation.
Seed 202605.""",
"""E1 is lowercased TF--IDF 1--2-grams (sublinear TF, min DF two, $L_2$,
100{,}000 features); validation selected $C = 10.0$ (ties down), refit once.
Seed 202605."""),
("""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}, new two-label head) over overlapping 512-token windows (50-token overlap):
three epochs, seed 202607, learning rate $2\\times10^{-5}$, weight
decay 0.01, warm-up ratio 0.1, gradient
accumulation.""",
"""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}, new head) over 512-token windows (50 overlap):
3 epochs, seed 202607, lr $2\\times10^{-5}$, decay 0.01, warmup 0.1."""),
("""Mean-logit pooling is primary; checkpoint selection uses validation mean-logit
accuracy only (majority vote is secondary). All
1{,}503 test documents and 9{,}576 windows are covered.""",
"""Mean-logit pooling is primary; checkpoint selection uses validation accuracy
only. 1{,}503 documents, 9{,}576 windows, all covered."""),
("""On 1{,}503 cases (Table~\\ref{tab:outcome}), E1 reached 0.61344 accuracy and 0.612342 macro-F1,
exceeding E2 mean-logit pooling at 0.596806 and 0.592358 (majority vote
0.6015/0.5937), all above
the 0.5017 majority baseline.""",
"""On 1{,}503 cases (Table~\\ref{tab:outcome}), E1 reached 0.61344/0.612342,
exceeding E2 mean-logit 0.596806/0.592358 (majority vote
0.6015/0.5937), all above
0.5017 majority."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p5: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
