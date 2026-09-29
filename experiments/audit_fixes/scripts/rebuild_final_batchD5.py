"""Rebuild batch D5: leftover compressions (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
("""(\\texttt{924a5bb9\\ldots dbdc773}) with a stable replay hash. The implementation passes 81 automated
research-pipeline tests (75 host-runnable plus 6
transformer/torch-only unit tests) and the documented
reproducibility checks (14/14 documentation checks and a freeze audit of 39 recorded
entries: 28 byte-exact, one line-ending-normalized, and 10 differing only in
non-scientific metadata, with all reported metrics verified identical;
per-file evidence in the repository audit). Separately, the
  local demo stack is covered by 8/8 Spring Boot service tests and 6/6 FastAPI
  wrapper tests; these exercise orchestration and contracts only, never the frozen
scientific results.""",
"""(\\texttt{924a5bb9\\ldots dbdc773}). The implementation passes 81
tests and the documented
checks (14/14 documentation; freeze audit of 39 entries:
28 byte-exact, one line-ending-normalized, 10 metadata-differing; all reported
metrics verified identical).
The demo stack is covered by 8/8 Spring Boot service tests and 6/6 FastAPI
wrapper tests."""),
("""Legal research operates in a domain where fluency is not evidence. A generated
response can be linguistically convincing while citing a judgment that does not
exist, attributing a passage to a real judgment that does not contain it, or
relying on law that was unavailable at the time the matter arose. Empirical
profiling of legal hallucination in large language models has established that
these failures are frequent rather than exceptional \\cite{dahl2024}, and related
work has probed how far explicit legal standards can be communicated to language
models at all \\cite{nay2023}.""",
"""Legal research operates in a domain where fluency is not evidence. A generated
response can cite a judgment that does not
exist, attribute a passage the judgment does not contain, or
rely on law unavailable at the time. Profiling of legal hallucination
in large language models shows
these failures are frequent rather than exceptional \\cite{dahl2024}, and how far explicit legal standards can be communicated to models remains open \\cite{nay2023}."""),
("""\\subsection{Legal retrieval, benchmarks, and temporal constraints}

COLIEE evaluates case-law and statute retrieval and entailment \\cite{coliee2023};
LegalBench measures LLM legal reasoning \\cite{legalbench2023}; CaseHOLD tests
holding selection and pre-training value \\cite{casehold2021}. Each uses one
fixed corpus and none requires a candidate to pre-date the query matter.""",
"""\\subsection{Legal retrieval and temporal constraints}

COLIEE, LegalBench, and CaseHOLD evaluate retrieval, reasoning, and holding
selection on single
fixed corpora with no pre-dating requirement \\cite{coliee2023,legalbench2023,casehold2021}."""),
("""\\subsection{Indian legal NLP and judgment prediction}

ILDC established Indian Supreme Court judgment prediction and
explanation as a benchmark task \\cite{malik2021}, supplying the fixed splits
and labels used here. InLegalBERT \\cite{paul2023} motivates our neural
baseline; practitioner-evaluated summarisation \\cite{shukla2022}
shows length and presentation are first-order concerns. None of""",
"""\\subsection{Indian legal NLP and judgment prediction}

ILDC established Indian Supreme Court judgment prediction and
explanation as a benchmark task \\cite{malik2021}; InLegalBERT \\cite{paul2023} motivates our neural
baseline; practitioner-evaluated summarisation \\cite{shukla2022}
shows length and presentation are first-order concerns. None of"""),
("""\\textbf{Future work.} An era-balanced key of 75--100 cases would support a
paired significance test (e.g., McNemar's); a blinded review with
independent raters and agreement reporting (e.g., Fleiss'
$\\kappa$) would replace the formative explanation evidence; hybrid
dense--sparse retrieval would test whether semantic retrieval closes
residual lexical misses under the present controls; and evidence-sensitive
uncertainty language would address the exposed
calibration weakness.""",
"""\\textbf{Future work.} An era-balanced key of 75--100 cases for paired testing;
blinded review with independent raters; hybrid
dense--sparse retrieval for residual lexical misses; and evidence-sensitive
uncertainty language."""),
("""A minimal connected local research demo (React 18 + TypeScript UI,
Spring Boot 3.2.5 orchestration API, FastAPI wrapper around the frozen
pipeline) exposes the E4 evidence path with bearer-token authentication,
per-request audit records, and experiment-metadata references; the FastAPI
layer delegates every research step to the frozen implementation and the
static frozen-artifact viewer is retained as a fallback. The stack binds to
loopback only and is not a production, multi-tenant, or autonomous system.""",
"""A minimal local research demo (React UI,
Spring Boot 3.2.5 API, FastAPI wrapper) exposes the E4 evidence path. The stack binds to
loopback only."""),
("""\\textbf{Scope.} Claims are deliberately narrow: no legal
correctness for retrieved authorities, no autonomous legal advisor, no
claim that evidence retrieval improves outcome prediction. Ours is a
researcher-facing prototype on four non-pooled
populations: 1{,}503 outcome cases, 30 frozen plus 7 additive source-verified
evidence cases in strata, and paired explanation examples (seven
formative author-reviewed pairs, superseded by a 14-case exploratory LLM
comparison).""",
"""\\textbf{Scope.} No legal
correctness for retrieved authorities, no autonomous legal advisor, no
claim that retrieval improves outcome prediction: a
researcher-facing prototype on four non-pooled
populations (1{,}503 outcome cases, 30 frozen plus 7 additive
evidence cases, paired explanation examples)."""),
("""There are exactly three research questions. \\textbf{RQ1:} Does grounding an
Indian legal AI workflow in retrieved legal evidence improve legal-research
reliability and relevant-evidence retrieval compared with a facts-only
legal-language baseline? The controlled comparison is E2 versus E3; E1 is a
traditional baseline reported for context. \\textbf{RQ2:} Does
provenance-constrained evidence selection and citation verification reduce
unsupported or unverifiable legal claims in the final output?
\\textbf{RQ3:} Can the proposed structured explanation format improve
human-verifiable transparency without materially degrading prediction or
retrieval performance?""",
"""There are exactly three research questions. \\textbf{RQ1:} Does grounding a
legal AI workflow in retrieved evidence improve reliability and retrieval against a facts-only
baseline (E2 versus E3; E1 for context)? \\textbf{RQ2:} Does
provenance-constrained selection and verification reduce
unsupported claims?
\\textbf{RQ3:} Can the structured explanation format improve
verifiable transparency?"""),
("""ILDC Single supplies fixed case-level splits and binary outcome labels: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test). After a shared sufficiency rule excluded 14 test records,
the held-out prediction population contains 1{,}503 cases.""",
"""ILDC Single supplies fixed case-level splits and binary outcome labels: 7{,}593 judgments (5{,}082 training, 994 validation,
1{,}517 test). After a shared sufficiency rule excluded 14 test records,
the prediction population contains 1{,}503 cases."""),
("""That conversion produced 5{,}391 syntactic candidates. \\textbf{Only 11 passed
content alignment; 5{,}380 were identifier-namespace collisions,} concentrated
in legacy material where similar numeric suffixes routinely denote entirely
different judgments. Trusting identifier equality here would silently merge
unrelated cases, corrupting both deduplication and leakage control.""",
"""That conversion produced 5{,}391 syntactic candidates. \\textbf{Only 11 passed
content alignment; 5{,}380 were identifier-namespace collisions.}"""),
("""We regard this audit as independently useful. It demonstrates that mechanically
similar ILDC and eCourts identifiers do not establish judgment identity, and it
supplies a content-based alternative reusable across answer-key validation,
development probes, leakage checks, and retrieval-time exclusion.""",
"""We regard this audit as independently useful: mechanically
similar ILDC and eCourts identifiers do not establish judgment identity."""),
("""The authority evaluation uses 30 ILDC fixed-test cases. Test membership was
confirmed before external verification. For each accepted case the query
judgment was inspected through a primary source or accepted eCourts mirror, one
earlier authority was recorded \\emph{independently of system retrieval}, and
that authority was reconciled to the corpus by stable source ID, normalised
citation, or normalised title plus exact date for parallel reporter forms.""",
"""The authority evaluation uses 30 ILDC fixed-test cases. For each, the query
judgment was inspected through a primary source or accepted eCourts mirror, one
earlier authority was recorded \\emph{independently of system retrieval}, and
reconciled by stable source ID, normalised
citation, or title plus exact date."""),
("""The sample is not era-balanced: five query cases are from the 1970s, 13 from the
1980s, nine from the 1990s, two from the 2000s, and one from the 2010s. The
1980s account for 43.3\\%. This concentration is a consequence of the source and
alignment gates rather than deliberate temporal sampling, and we treat it as a
limitation (Section~\\ref{sec:limits}).""",
"""The sample is not era-balanced: five query cases are from the 1970s, 13 from the
1980s, nine from the 1990s, two from the 2000s, and one from the 2010s
(1980s: 43.3\\%), a consequence of the source and
alignment gates (Section~\\ref{sec:limits})."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print(f"D5: {len(EDITS) - len(fails)}/{len(EDITS)}, fails: {fails}")
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
