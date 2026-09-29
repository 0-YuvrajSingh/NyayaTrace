"""6-page compression batch 1: abstract/intro/related/method (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_6page.tex").read_text(encoding="utf-8")

EDITS = [
("""AI-assisted legal research fails in ways that fluent output conceals: a cited
authority may not exist, may lack the attributed passage, may post-date
the matter, or may never have been retrieved. A 2026 Supreme Court of India
ruling (2026 INSC 668) overturned tribunal findings built on exactly these
defects. We present an
evidence pipeline for
historical Indian Supreme Court judgments in which every displayed citation is
temporally eligible, provenance-bound, and mechanically verifiable, with outcome
prediction kept separate. We report three findings on combined 37 cases
(frozen 30 plus 7 extension, in strata).""",
"""Fluent legal output conceals failures: nonexistent authorities, misattributed
passages, post-dated or unretrieved matter. A 2026 Supreme Court of India
ruling (2026 INSC 668) overturned tribunal findings built on exactly these
defects. We present an
evidence pipeline for
Indian Supreme Court judgments where every displayed citation is
temporally eligible, provenance-bound, and mechanically verifiable, with
prediction kept separate. Three findings on combined 37 cases
(frozen 30 plus 7 extension, in strata) follow."""),
("""Legal research rewards fluency over evidence: generated
responses cite nonexistent judgments, misattribute passages, or
invoke unavailable law. Such hallucinations are frequent, not exceptional
\\cite{dahl2024}, and communicating legal standards to models remains open
\\cite{nay2023}.""",
"""Legal research rewards fluency over evidence: fabricated citations and
unavailable law are frequent, not exceptional
\\cite{dahl2024}; communicating legal standards to models remains open
\\cite{nay2023}."""),
("""India set aside tribunal decisions after identifying nonexistent authorities,
incorrect citations, and fabricated passages apparently produced through
AI-assisted research \\cite{poojasingh2026}.""",
"""India set aside tribunal decisions resting on nonexistent authorities,
incorrect citations, and apparently AI-fabricated passages \\cite{poojasingh2026}."""),
("""This paper treats that requirement as the design constraint:
retrieved facts carry stable
locators, duplicates are excluded, only verbatim passages are rendered,
and each citation is verified against corpus and retrieval run.""",
"""We therefore require: stable locators on retrieved facts, duplicate
exclusion, verbatim-only rendering,
and per-citation verification against corpus and retrieval run."""),
("""\\item \\textbf{A quantified cross-corpus identity failure and its remedy.}
\\texttt{YYYY INSC N} to \\texttt{YYYY\\_N} conversion produced 5{,}391 syntactic candidates, of which only 11 passed
content alignment (Section~\\ref{sec:alignment}).""",
"""\\item \\textbf{Cross-corpus identity failure, quantified and remedied.}
\\texttt{YYYY INSC N} to \\texttt{YYYY\\_N} conversion: 5{,}391 syntactic candidates, 11
passing content alignment (Section~\\ref{sec:alignment})."""),
("""\\item \\textbf{Pre-ranking temporal eligibility.} Historical
availability as a predicate inside the BM25 candidate relation, so ineligible judgments cannot consume retrieval depth
(Section~\\ref{sec:e3}): Recall@5 moved
from 5/30 to 12/30 without regressing any prior success.""",
"""\\item \\textbf{Pre-ranking temporal eligibility.} Availability as a predicate
inside BM25 retrieval (Section~\\ref{sec:e3}): Recall@5
5/30 to 12/30 with no regressions."""),
("""ILDC \\cite{malik2021} supplies splits; InLegalBERT \\cite{paul2023} motivates the neural baseline;
TaxFlow \\cite{taxflow2026} addresses statutory validity; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} target validity and event ordering.""",
"""ILDC \\cite{malik2021} supplies splits; InLegalBERT \\cite{paul2023} the neural baseline;
TaxFlow \\cite{taxflow2026} statutory validity; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} validity and event ordering."""),
("""We claim neither the first legal RAG system, nor the first
Indian legal model, nor the first temporal legal benchmark: the contribution is
the reproducible combination of content-alignment gating,
conservative pre-ranking eligibility, exact retrieval-run
verification, and separate recovery-versus-validity reporting on a source-first key.
Jurisdictions, tasks, corpora, and denominators differ, so no external system is
used as a numerical baseline.""",
"""We claim no first-system novelty: the contribution is
content-alignment gating,
pre-ranking eligibility, retrieval-run
verification, and separate recovery-versus-validity reporting. Tasks, corpora, and
denominators differ, so no external numerical baseline is used."""),
("""There are three research questions. \\textbf{RQ1:} Does grounding a
legal AI workflow in retrieved evidence improve reliability and retrieval against a facts-only
baseline (E2 versus E3; E1 for context)? \\textbf{RQ2:} Does
provenance-constrained selection and verification reduce
unsupported claims?
\\textbf{RQ3:} Can the structured explanation format improve
verifiable transparency?

For RQ3, the implemented comparison holds the underlying evidence and citations
constant and compares structured with unstructured presentation
(transparency only).""",
"""Three questions. \\textbf{RQ1:} Does retrieved evidence improve reliability and retrieval over a facts-only
baseline (E2 versus E3; E1 for context)? \\textbf{RQ2:} Does
provenance-constrained verification reduce
unsupported claims?
\\textbf{RQ3:} Can structured presentation improve
verifiable transparency (evidence held constant)?"""),
("""ILDC Single supplies fixed splits and binary labels: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test); after a shared sufficiency rule excluded 14 test records,
1{,}503 cases remain.""",
"""ILDC Single: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test); a shared sufficiency rule excluded 14 test records,
leaving 1{,}503 cases."""),
("""The evidence corpus is an eCourts-derived collection of Indian Supreme Court
judgments covering 1950--2020. Of 39{,}069 English
PDF instances, 39{,}066 accepted PDFs yielded
2{,}343{,}435 labelled chunks, of which 2{,}036{,}981 unique chunks were loaded
into a PostgreSQL provenance store and a SQLite FTS5 BM25 index.""",
"""The eCourts-derived evidence corpus (Indian Supreme Court,
1950--2020): 39{,}069 English
PDF instances, 39{,}066 accepted, yielding
2{,}343{,}435 chunks, of which 2{,}036{,}981 unique chunks were loaded
into PostgreSQL provenance and a SQLite FTS5 BM25 index."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("6p1: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_6page.tex").write_text(t, encoding="utf-8")
