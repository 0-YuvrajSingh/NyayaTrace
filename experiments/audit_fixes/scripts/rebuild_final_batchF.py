"""Rebuild batch F: final prose cuts (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
("""Legal research operates in a domain where fluency is not evidence. A generated
response can cite a judgment that does not
exist, attribute a passage the judgment does not contain, or
rely on law unavailable at the time. Profiling of legal hallucination
in large language models shows
these failures are frequent rather than exceptional \\cite{dahl2024}, and how far explicit legal standards can be communicated to models remains open \\cite{nay2023}.""",
"""Legal research rewards fluency over evidence: generated
responses cite nonexistent judgments, misattribute passages, or
invoke unavailable law. Such hallucinations are frequent, not exceptional
\\cite{dahl2024}, and communicating legal standards to models remains open
\\cite{nay2023}."""),
("""The central empirical observation is a dissociation. All 185 displayed citations
cleared grounding, provenance, duplicate, and temporal checks, with no
unsupported claim; at the same time, 17 of 37
verified expected authorities never appeared in the top 100.""",
"""The central finding is a dissociation: all 185 displayed citations
cleared verification with no
unsupported claim, yet 17 of 37
expected authorities never appeared in the top 100."""),
("""\\subsection{Legal retrieval and temporal constraints}

COLIEE, LegalBench, and CaseHOLD evaluate retrieval, reasoning, and holding
selection on single
fixed corpora with no pre-dating requirement \\cite{coliee2023,legalbench2023,casehold2021}.
TaxFlow applies hybrid RAG with validity filtering to Indian tax-law
QA \\cite{taxflow2026}; CaseFacts frames claim
verification with evolving validity \\cite{casefacts2026};
LexTime benchmarks temporal event ordering
\\cite{lextime2025}. RAG
established retrieval as explicit non-parametric evidence
\\cite{lewis2020}; BM25 supplies the sparse ranking basis \\cite{robertson2009}
and Tesseract the OCR engine for corpus repair \\cite{smith2007}.""",
"""\\subsection{Legal retrieval and temporal constraints}

COLIEE, LegalBench, and CaseHOLD evaluate retrieval and reasoning on single
fixed corpora with no pre-dating requirement \\cite{coliee2023,legalbench2023,casehold2021}.
TaxFlow adds validity filtering for Indian tax-law QA \\cite{taxflow2026};
CaseFacts and LexTime target evolving validity and event ordering
\\cite{casefacts2026,lextime2025}. RAG
established retrieval as explicit evidence
\\cite{lewis2020}; BM25 supplies the ranking basis \\cite{robertson2009}
and Tesseract the OCR engine \\cite{smith2007}."""),
("""We use two corpora for different experimental purposes.
ILDC Single supplies fixed case-level splits and binary outcome labels: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test). After a shared sufficiency rule excluded 14 test records,
the prediction population contains 1{,}503 cases.""",
"""ILDC Single supplies fixed splits and binary labels: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test); after a shared sufficiency rule excluded 14 test records,
1{,}503 cases remain."""),
("""A full audit found the stored text valid UTF-8, but 15 PDF instances
(representing 14 source IDs) had missing or badly corrupted embedded text.""",
"""A full audit found valid UTF-8 text except 15 PDF instances
(14 source IDs) with missing or corrupted embedded text."""),
("""The evidence task decomposes into three separable questions: recovery (is the
expected authority in the top 100 and among the five displayed?),
integrity (does each displayed citation reproduce a real retrieved passage with
exact provenance, avoiding the query and duplicates, under the temporal rule?),
and presentation (does the structured format aid inspection?).""",
"""The evidence task decomposes into recovery (expected authority in the top 100
and among the five displayed?),
integrity (each citation a real retrieved passage with
exact provenance, avoiding query/duplicates, under the temporal rule?),
and presentation (does structure aid inspection?)."""),
("""Outcome prediction is a secondary evaluation capability, not a fourth research
question. It is reported on its own
population and never pooled with the evidence measures, so that a classification
score cannot substitute for evidence quality and a traceable citation cannot be
mistaken for complete authority recovery. Table~\\ref{tab:defs} fixes the
operational definitions and pass/fail criteria.""",
"""Outcome prediction is secondary, reported on its own
population and never pooled with evidence measures. Table~\\ref{tab:defs} fixes
definitions and pass/fail criteria."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("F: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
