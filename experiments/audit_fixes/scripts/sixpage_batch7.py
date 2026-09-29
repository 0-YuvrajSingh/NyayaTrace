"""6-page compression batch 7 (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""We report three findings on combined 37 cases
(frozen 30 plus 7 extension, in strata).""",
"""Three findings on combined 37 cases
(frozen 30 plus 7 extension, in strata) follow."""),
("""Legal research rewards fluency over evidence: fabricated citations and
unavailable law are frequent, not exceptional
\\cite{dahl2024}; communicating legal standards to models remains open
\\cite{nay2023}.""",
"""Legal fluency outruns evidence: fabricated citations are frequent
\\cite{dahl2024}; communicating legal standards to models remains open
\\cite{nay2023}."""),
("""We therefore require stable locators, duplicate
exclusion, verbatim-only rendering,
and per-citation verification.""",
"""We therefore require stable locators, no duplicates,
verbatim-only rendering, per-citation verification."""),
("""Central dissociation: 185 displayed citations
verified, zero unsupported,
yet 17 of 37
expected authorities absent from the top 100.""",
"""Central dissociation: 185 citations
verified, yet 17 of 37
authorities absent from the top 100."""),
("""\\item \\textbf{Identity failure, quantified and remedied.}
\\texttt{YYYY INSC N} to \\texttt{YYYY\\_N}: 5{,}391 candidates, 11
passing alignment (Section~\\ref{sec:alignment}).""",
"""\\item \\textbf{Identity failure, quantified.}
\\texttt{YYYY INSC N} to \\texttt{YYYY\\_N}: 5{,}391 candidates, 11
passing alignment (Section~\\ref{sec:alignment})."""),
("""ILDC \\cite{malik2021} supplies splits; InLegalBERT \\cite{paul2023} the neural baseline;
TaxFlow \\cite{taxflow2026} statutory validity; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} validity and event ordering.""",
"""ILDC \\cite{malik2021} splits; InLegalBERT \\cite{paul2023} baseline;
TaxFlow \\cite{taxflow2026} validity; CaseFacts \\cite{casefacts2026}, LexTime
\\cite{lextime2025} ordering."""),
("""Three questions. \\textbf{RQ1:} Retrieved evidence versus facts-only
baseline (E2 versus E3; E1 for context)? \\textbf{RQ2:} Does
verification reduce
unsupported claims?
\\textbf{RQ3:} Does structured presentation improve
transparency (evidence held constant)?""",
"""\\textbf{RQ1:} Retrieved evidence versus facts-only
(E2 versus E3; E1 context)? \\textbf{RQ2:} Less
unsupported claims?
\\textbf{RQ3:} Better
transparency (evidence held constant)?"""),
("""A later extension verified seven further fixed-test cases
(\\texttt{1990\\_234}, \\texttt{1990\\_256}, \\texttt{1990\\_324},
\\texttt{1991\\_136}, \\texttt{1991\\_87}, \\texttt{1992\\_286},
\\texttt{1993\\_90}); three further
candidates were held back. The combined 37 cases are a later expanded analysis;
results retain Base-30, Extension-7, and Combined-37 strata.""",
"""A later extension verified seven further cases
(\\texttt{1990\\_234}, \\texttt{1990\\_256}, \\texttt{1990\\_324},
\\texttt{1991\\_136}, \\texttt{1991\\_87}, \\texttt{1992\\_286},
\\texttt{1993\\_90}); three
held back. Combined 37 is a later expanded analysis;
strata retained."""),
("""E1 and E2 share facts-only extraction (\\texttt{ildc-predecision-facts-v1}, pre-dispositive-cue text
capped at 60\\%): cases below 10\\% retention or 100 words are excluded;
validation-only selection, one held-out test evaluation.""",
"""E1/E2 share facts-only extraction (\\texttt{ildc-predecision-facts-v1},
pre-dispositive text, 60\\% cap): exclusions below 10\\%/100 words;
validation-only selection, one test evaluation."""),
("""E1 is lowercased TF--IDF 1--2-grams (sublinear TF, min DF two, $L_2$,
100{,}000 features); validation selected $C = 10.0$ (ties down), refit once.
Seed 202605.""",
"""E1: TF--IDF 1--2-grams (sublinear TF, min DF 2, $L_2$,
100k features); $C = 10.0$ (ties down), refit once.
Seed 202605."""),
("""E2 fine-tunes \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}, new head) over 512-token windows (50 overlap):
3 epochs, seed 202607, lr $2\\times10^{-5}$, decay 0.01, warmup 0.1.""",
"""E2: \\texttt{law-ai/InLegalBERT} (revision
\\texttt{b5ecfed8}, new head), 512-token windows (50 overlap):
3 epochs, seed 202607, lr $2\\times10^{-5}$, decay 0.01, warmup 0.1."""),
("""Mean-logit pooling is primary; checkpoint selection uses validation accuracy
only. 1{,}503 documents, 9{,}576 windows, all covered.""",
"""Mean-logit pooling primary; validation-selected checkpoint.
1{,}503 documents, 9{,}576 windows."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p7: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
