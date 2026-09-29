"""Rebuild batch D2: compression edits (non-aborting)."""
from pathlib import Path

R = Path("/repo")
t = (R / "paper_master_final.tex").read_text(encoding="utf-8")

EDITS = [
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
("""ILDC \\cite{malik2021} supplies the prediction
setting and splits; InLegalBERT \\cite{paul2023} motivates the neural baseline
(corrected here for truncation); TaxFlow \\cite{taxflow2026} shares
legal-retrieval concerns but addresses statutory validity rather than precedent
identity and passage provenance; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} target open-retrieval validity and event ordering, whereas we
enforce availability through metadata before ranking.""",
"""ILDC \\cite{malik2021} supplies the prediction
setting and splits; InLegalBERT \\cite{paul2023} motivates the neural baseline;
TaxFlow \\cite{taxflow2026} addresses statutory validity rather than precedent
identity and passage provenance; CaseFacts \\cite{casefacts2026} and LexTime
\\cite{lextime2025} target open-retrieval validity and event ordering, whereas we
enforce availability through metadata before ranking."""),
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
("""Mean pooling of window logits before softmax is the primary rule, and checkpoint
selection uses validation document-level mean-logit accuracy only. Majority vote
is reported as a secondary comparison, not a post-hoc selection rule. All
1{,}503 eligible test documents and 9{,}576 test windows are covered.""",
"""Mean pooling of window logits before softmax is the primary rule, and checkpoint
selection uses validation document-level mean-logit accuracy only (majority vote
is a secondary comparison, not a selection rule). All
1{,}503 eligible test documents and 9{,}576 test windows are covered."""),
("""On the 1{,}503-case population (Table~\\ref{tab:outcome}), sparse E1 reached accuracy 0.61344 and macro-F1 0.612342,
exceeding corrected E2 mean-logit pooling at 0.596806 and 0.592358. E2's secondary
majority-vote aggregation reached 0.6015 and 0.5937. All primary models exceeded
the 0.5017 majority-class accuracy.""",
"""On the 1{,}503-case population (Table~\\ref{tab:outcome}), sparse E1 reached accuracy 0.61344 and macro-F1 0.612342,
exceeding corrected E2 mean-logit pooling at 0.596806 and 0.592358 (majority vote
0.6015 and 0.5937). All primary models exceeded
the 0.5017 majority-class accuracy."""),
("""On the separate 30-case subset, evidence-augmented E3 and verified E4 both
reached accuracy 0.666667 and macro-F1 0.603175, with identical confusion matrices.
On the combined 37 cases the same shared predictor reaches accuracy 0.648649 and
macro-F1 0.607347 with confusion matrix [[6,3],[10,18]], again identical for E3
and E4 (Table~\\ref{tab:rq1strata}).
\\textbf{The equality is expected and is not evidence that verification is
redundant:} with no evidence rejected, the predictor received an identical
input; E4's contribution is control, traceability, and explanation. Had
verification rejected evidence, the reported pair would diverge visibly.""",
"""On the separate 30-case subset, E3 and E4 both
reached accuracy 0.666667 and macro-F1 0.603175, with identical confusion matrices.
On the combined 37 the same predictor reaches 0.648649 and
0.607347 with confusion matrix [[6,3],[10,18]], again identical for E3
and E4 (Table~\\ref{tab:rq1strata}).
\\textbf{The equality is expected:} with no evidence rejected, the predictor received an identical
input."""),
("""The principal RQ1 result uses the combined 37-case population
(Table~\\ref{tab:rq1strata}). The seven extension cases contribute no
additional top-5 recovery (0/7) but five further top-100 recoveries at ranks
14, 16, 26, 32, and 89, with two absent; their displayed citations are
likewise fully verified (35/35). The combined figures are therefore Recall@5
12/37 $=$ 0.324324 and Recall@100 20/37 $=$ 0.540541 over 185 displayed
citations. The lower combined Recall@5 is descriptive of the added stratum,
not evidence about the base configuration, and the frozen 30-case result
above is retained unchanged alongside it.""",
"""The principal RQ1 result uses the combined 37-case population
(Table~\\ref{tab:rq1strata}). The seven extension cases contribute no
additional top-5 recovery (0/7) but five further top-100 recoveries at ranks
14, 16, 26, 32, and 89, with two absent; their displayed citations are
likewise fully verified (35/35). The combined figures are Recall@5
12/37 $=$ 0.324324 and Recall@100 20/37 $=$ 0.540541 over 185 displayed
citations. The lower combined Recall@5 describes the added stratum, not the base configuration."""),
("""Figure~\\ref{fig:funnel} shows the recovery funnel. Base-30 integrity is
150/150 grounded and provenance-valid with 0/150 temporal violations and 0/30
unsupported claims (Table~\\ref{tab:integrity}, Fig.~\\ref{fig:integrity});
the candidate log held 3{,}000/3{,}000 eligible candidates, and a five-case
faithfulness check resolved every reference to its persisted chunk. Combined-37
holds the same profile at 185/185, 0/185, and 0/37.""",
"""Figure~\\ref{fig:funnel} shows the recovery funnel. Base-30 integrity is
150/150 grounded and provenance-valid with 0/150 temporal violations and 0/30
unsupported claims (Table~\\ref{tab:integrity}, Fig.~\\ref{fig:integrity});
Combined-37 holds the same profile at 185/185, 0/185, and 0/37."""),
("""\\textbf{This is the paper's central result.} Verification success and authority
recovery are dissociated: the system verified everything it displayed (185/185
combined; 150/150 on the frozen base) while recovering the expected authority
in 20 of 37 cases at $k{=}100$ (15/30 base). Neither number alone
describes the system. A reviewer told only that all displayed citations are valid
would over-trust it; a reviewer told only that Recall@100 is 0.54 would miss
that nothing displayed was fabricated, misattributed, or anachronistic.""",
"""\\textbf{This is the paper's central result.} The system verified everything it displayed (185/185
combined; 150/150 base) while recovering the expected authority
in 20 of 37 cases at $k{=}100$ (15/30 base)."""),
]
fails = []
for i, (old, new) in enumerate(EDITS):
    c = t.count(old)
    if c != 1:
        fails.append((i, c))
        continue
    t = t.replace(old, new)
print(f"D2: {len(EDITS) - len(fails)}/{len(EDITS)}, fails: {fails}")
(R / "paper_master_final.tex").write_text(t, encoding="utf-8")
