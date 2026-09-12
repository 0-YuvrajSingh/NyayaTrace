# Content Only Publication Readiness Report

## Scope and authority

This pass used `Indian_Legal_XAI.docx` (Canonical Project Specification --
Document 3 Final) as the scope authority and the repository's frozen experiment
artifacts as the authority for measured results. It did not change the document
class, page layout, figures, tables, experiment implementation, datasets,
metrics, or research objectives.

## Changes made

1. Replaced all five author emails with the supplied addresses and removed
   `(Supervisor)` from Kriti Mishra's author name.
2. Replaced `preregistered frozen base` with `original frozen base`.
3. Made the E1--E4 roles explicit: E1 is the TF--IDF plus logistic-regression
   outcome baseline; E2 is the facts-only InLegalBERT outcome baseline; E3 is
   retrieval/evidence-grounded; and E4 is the verification, provenance, and
   structured-explanation bundle. The text now explicitly says that E2 is not a
   retrieval baseline, retrieval is evaluated against the predefined
   authority/evidence key, and outcome prediction is secondary.
4. Clarified that the evidence renderer, rather than the whole system, is
   extractive and non-inferential; outcome prediction is produced by the
   separate prediction branch.
5. Clarified that evidence-augmented E3/E4 prediction is descriptive, applies
   the frozen E2 checkpoint at inference time, and uses a population distinct
   from the 1,503-case outcome population.
6. Kept all three frozen research questions unchanged in substance. Added an
   interpretation note that the implemented RQ3 comparison holds evidence and
   citations constant and evaluates presentation transparency only; it does not
   independently establish a prediction or retrieval performance effect.
7. Corrected the RQ2 interpretation: no live selected citation was rejected by
   E4, so there is no empirical E3-to-E4 reduction magnitude on the live set.
   The text identifies this as a ceiling effect and states that the unchanged
   verifier rejected each positive-control class 37/37.
8. Corrected the retrieval failure-analysis claim from a dominant causal claim
   to a prominent unresolved cause in the analysed failures. The limitations
   section now also says the comparison does not establish causal attribution.
9. Expanded the RQ3 accounting to state 14 cases, four evaluators, 56
   case-rater pairs, 112 condition instances, 560 dimension-level scores, 56
   forced preferences, 56/56 structured preference, and the reported overall
   difference of +1.95 (4.66 versus 2.71). It remains an exploratory LLM-rater
   presentation evaluation, not independent human-subject evidence.
10. Replaced the self-review overstatement with the specified cautious wording
    about generic uncertainty language and evidence quality.
11. Replaced the future-work guarantee with a planned, approximately 75--100
    case paired test subject to sufficient discordant pairs.
12. Restored the requested artifact precision where the manuscript had rounded
    final E1, E2 mean-logit, E3/E4, combined E3/E4, and combined-retrieval
    values. No measured result changed.
13. Audited the embedded bibliography. All 15 cited keys resolve to a
    `\bibitem`, and every `\bibitem` is cited. Corrected the TaxFlow author
    initials/order to match the publisher's author list; title, year, venue, and
    article identifier remain unchanged.

## Issues detected but deliberately not changed

- `References.bib` is not present in the repository; the operative bibliography
  is embedded in `paper_master.tex`. No separate `.bib` file was created.
- The manuscript already uses `IEEEtran`. This pass did not migrate, redesign,
  or otherwise modify that pre-existing format.
- The bibliography's working order-copy URL for *Pooja Ramesh Singh* was left in
  place; it resolves to the cited judgment. No source was replaced merely to
  change its hosting location.
- Dense/hybrid retrieval appears only in related work and future work, not as an
  implemented experiment. Other out-of-scope concepts were likewise retained
  only where clearly marked as limitations, governance boundaries, related work,
  or future work.
- No TeX compiler is available in the active environment, so no new PDF was
  generated. The TeX source received source-level consistency checks only; this
  content-only pass does not modify layout.

## Required confirmations

- The three frozen RQs remain unchanged in substance.
- No experiment, dataset, metric, architecture component, or research objective
  was added.
- Reported numerical results are unchanged and were checked against the frozen
  E1/E2, RQ1, RQ2, and RQ3 artifacts. Precision-only corrections now match the
  authoritative values where updated.
- All five figures and all tables remain logically consistent with the corrected
  narrative; no figure or table was redesigned or altered.
- Author names and the five supplied email addresses are correct. Kriti Mishra
  appears without a supervisor designation in the author name.
- The paper makes no unsupported positive scope claim: it does not claim legal
  correctness, autonomous legal decision-making or advice, current-case,
  multilingual, High Court/lower-court generalization, implemented dense/hybrid
  retrieval, GraphRAG, graph databases, multi-agent reasoning, foundation-model
  benchmarking, production SaaS, human-subject evidence from the LLM-rater
  study, provenance-based causal attribution, legal certainty from model
  confidence, or prediction improvement from evidence retrieval.
