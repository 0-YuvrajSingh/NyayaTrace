"""Rebuild batch G: final micro-cuts (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
("""7-case extension, analysed in strata). First, naive identifier matching between ILDC and an eCourts-derived
judgment archive is unsafe: of 5{,}391 syntactic matches only 11
survived alignment.""",
"""7-case extension, in strata). First, naive ILDC--eCourts identifier matching is unsafe:
11 of 5{,}391 syntactic matches survived alignment."""),
("""This paper treats that requirement as the primary design constraint over
historical Indian Supreme Court judgments: retrieved facts carry stable
locators, duplicates are excluded, only verbatim passages are rendered,
and each citation is verified against the persisted corpus and retrieval run.""",
"""This paper treats that requirement as the primary design constraint:
retrieved facts carry stable
locators, duplicates are excluded, only verbatim passages are rendered,
and each citation is verified against corpus and retrieval run."""),
("""ILDC \\cite{malik2021} supplies the prediction
setting and splits; InLegalBERT \\cite{paul2023} motivates the neural baseline;
TaxFlow \\cite{taxflow2026} addresses statutory validity; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} target open-retrieval validity and event ordering.""",
"""ILDC \\cite{malik2021} supplies splits; InLegalBERT \\cite{paul2023} motivates the neural baseline;
TaxFlow \\cite{taxflow2026} addresses statutory validity; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} target validity and event ordering."""),
("""A later additive extension verified seven further fixed-test cases
(\\texttt{1990\\_234}, \\texttt{1990\\_256}, \\texttt{1990\\_324},
\\texttt{1991\\_136}, \\texttt{1991\\_87}, \\texttt{1992\\_286},
\\texttt{1993\\_90}) under the
same gates, without modifying the original 30-case key.
Three further candidates were held back as needing review. The combined 37-case
population is a later expanded analysis, not the frozen base; results below
retain Base-30, Extension-7, and Combined-37 strata.""",
"""A later extension verified seven further fixed-test cases
(\\texttt{1990\\_234}, \\texttt{1990\\_256}, \\texttt{1990\\_324},
\\texttt{1991\\_136}, \\texttt{1991\\_87}, \\texttt{1992\\_286},
\\texttt{1993\\_90}); three further
candidates were held back. The combined 37 cases are a later expanded analysis;
results retain Base-30, Extension-7, and Combined-37 strata."""),
("""E1 and E2 share the extraction configuration \\texttt{ildc-\\allowbreak predecision-\\allowbreak facts-\\allowbreak v1}: text preceding the earlier of a recognised dispositive cue
and 60\\% of the document, sentence-aligned where possible. Cases below 10\\% retention or 100 words are excluded.
Neither prediction path uses retrieval. Selection uses
validation data only; the held-out test split is evaluated once.""",
"""E1 and E2 share facts-only extraction (\\texttt{ildc-predecision-facts-v1}): text preceding a dispositive cue
and 60\\% of the document. Cases below 10\\% retention or 100 words are excluded;
selection uses
validation only, with one held-out test evaluation."""),
("""The query builder (\\texttt{tfidf-segment-salient-terms-v1}) segments the facts-only input, removes procedural-report boilerplate, scores terms
deterministically, retains section/article cues, and emits at most 32 unique
terms for a SQLite FTS5 BM25 index backed by PostgreSQL provenance.""",
"""The query builder (\\texttt{tfidf-segment-salient-terms-v1}) emits at most 32 salient
terms for a SQLite FTS5 BM25 index backed by PostgreSQL provenance."""),
("""The principal RQ3 evaluation is a blinded exploratory comparison
by four LLM raters (Gemini, Claude Sonnet 4.6, DeepSeek, GPT-5.6 Luna) over 14
paired cases on five transparency
dimensions (1--5) with a forced preference. The structured presentation was preferred in 56/56 evaluations""",
"""The principal RQ3 evaluation is a blinded exploratory comparison
by four LLM raters over 14
paired cases on five transparency
dimensions with a forced preference. The structured presentation was preferred in 56/56 evaluations"""),
("""DeepSeek and GPT-5.6 Luna produced byte-identical
rating vectors, retained separately rather than
merged, so the unanimity partly reflects duplicated outputs. The seven-case self-review (7/7 structured) is formative,
non-independent evidence superseded above; its durable negative output is that generic
uncertainty wording did not adapt to
\\texttt{2013\\_35}.""",
"""Two raters produced byte-identical
vectors, retained separately;
the seven-case self-review (7/7) is formative,
non-independent evidence superseded above."""),
("""\\textbf{Scope.} English-language Indian Supreme Court judgments
only; no other languages, lower courts,
statutes, or cross-jurisdictional transfer.""",
"""\\textbf{Scope.} English-language Indian Supreme Court judgments
only."""),
("""\\textbf{Year-level temporal granularity.} Query dates have
year-level precision only, so any same-year candidate
is conservatively excluded.""",
"""\\textbf{Year-level granularity.} Query dates have
year-level precision only, so same-year candidates
are conservatively excluded."""),
("""\\textbf{Bundled verification.} E4 checks several integrity properties together
and cannot isolate any single component's contribution.""",
"""\\textbf{Bundled verification.} E4 checks integrity properties together
and cannot isolate single-component contributions."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print("G: %d/%d, fails: %s" % (len(EDITS) - len(fails), len(EDITS), fails))
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
