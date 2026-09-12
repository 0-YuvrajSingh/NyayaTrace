# Phase 2.8 — Final consistency audit (narrow pass; no new research)

## 1. Issue 1 — E3/E4 prediction population: RESOLVED (artifact-governed)

- Artifact showed: `rq1_results.json` strata carry genuine per-stratum E3
  predictions (base30 0.666667/0.603175 CM [[4,3],[7,16]]; ext7
  0.571429/0.571429 CM [[2,0],[3,2]]; combined37 0.648649/0.607347 CM
  [[6,3],[10,18]]); `rq2_results.json` confirms E4 identical on combined37.
  E3 prediction was computed for all three strata, not base-only.
- Manuscript previously said (§Method): predictions "reported descriptively
  on the 30-case subset" with no combined statement.
- Correction: Method now states descriptively on base-30 AND combined-37
  (1,503 baselines kept separate); §Results adds the combined sentence
  (0.6486/0.6073 CM [[6,3],[10,18]], E3==E4) pointing at Table IV.
- Authoritative population: both strata reported; combined37 is the
  principal RQ1 reporting level, base30 retained alongside.

## 2. Issue 2 — unsupported-claims denominator: RESOLVED

- Previous: Table V "Unsupported claims 0 — 0 of 150" (citation-level
  denominator on a case-level metric).
- Corrected: "0 of 30 cases" (`rq2_results.json`:
  d_unsupported_claim_rate num 0 den 30; combined 0/37).
- Verified in compiled PDF text: Table V row reads "Unsupported claims 0
  0 of 30 cases"; all other unsupported mentions carry 0/30 or 0/37.

## 3. Denominator audit (~90 occurrences scanned)

- Fixed additionally: abstract, intro dissociation, §Results base paragraph,
  and conclusion now attach case denominators to every unsupported-claims
  mention (0/30 base, 0/37 combined). Table IV + surrounding prose +
  captions carry explicit Base-30/Extension-7/Combined-37 labels with
  matching numerators (12/30, 15/30, 0/7, 5/7, 12/37, 20/37, 150, 35, 185).
- No other mismatches: R@5/R@100, precision/recall/F1, groundedness,
  provenance, temporal, accuracy/Macro-F1, n= and citation counts all match
  artifacts with populations identified; valid denominators left untouched.

## 4. Figure/table audit

Fig 1 (n=1,503), Fig 2 (combined-37 funnel 12/8/17), Fig 3 (combined-37,
185), Fig 4 (historical dev/base labels), Fig 5 (14×4 LLM) — captions,
axes, and prose verified against artifacts; Table IV (strata) and Table V
(base-labeled) verified in the rendered PDF. No regeneration needed.

## 5. RQ audit

Exactly RQ1/RQ2/RQ3 canonical; zero RQ4; E1 contextual; RQ3 intact
(14 cases, 4 LLM raters, 112 ratings, 56 prefs 56/56 structured, 5 dims,
exploratory/non-human, anomaly disclosed, n=7 formative-only).

## 6. Final status: PASS

Compilation clean (Tectonic; only cosmetic Underfull warnings); 11-page
PDF visually inspected (abstract, tables IV–V, figures, RQ3, references);
tests 75 passed; frozen results/keys/code/configs untouched (paper + PDF +
this audit only).
