# RQ2 design audit — what E3 vs E4 actually differ in (read from code, 2026-09-11)

Scripts: `scripts/run_evidence_pipeline.py` (E3) vs
`scripts/run_grounded_answer_pipeline.py` (E4). Shared library:
`src/legal_xai/{evidence_pipeline,retrieval,temporal,alignment,
grounded_answer,citation_verifier,evidence_augmented_prediction}.py`.

## 1. Evidence selection differences

NONE. Both call the identical functions with the identical frozen config
(`config/evidence_selection.json`, `week11-bm25-salient-terms-preranked-
temporal-v3`, k=100, top-5, 1-per-source, salient-tfidf query, pre-rank
temporal predicate, alignment-gated dedup). E3 and E4 therefore see the
same candidates and select the same evidence by construction. Stated
explicitly: the RQ2 controlled change is NOT selection.

## 2. Provenance checks

E3 performs none post-selection. E4's `verify_rendered_explanation`
(`run_grounded_answer_pipeline.py:21-57`) reloads per-chunk provenance
(source/case/citation/date/court/pdf/page/char locators + text) from
`corpus_chunks` and the eligible run-membership set from
`retrieval_results`, then enforces exact reproduction through
`verify_answer_citations`.

## 3. Citation validation

E3: absent. E4: 5-check contract (`citation_verifier.py:113-174`) —
corpus-chunk existence, exact passage+provenance match, run membership,
duplicate/near-duplicate exclusion, temporal eligibility — plus
unsupported-authority-field rejection. Fail-closed: ANY failure raises
`ValueError`, so no E4 output exists for a violating case.

## 4. Temporal checks

Definition shared (`temporal.py`, precedent_year < query_year, pre-rank).
E3 enforces it at selection (SQL predicate + recheck). E4 re-enforces it
per displayed citation inside the verifier. Same rule, second enforcement
point; E4 additionally fails the whole answer on any violation.

## 5. Structured explanation generation

E3: none (evidence list + prediction only). E4: extract-only renderer
(`grounded_answer.py:render_grounded_answer`, version
`week10-verified-explanation-renderer-v1`, fixed 5-section order,
non-inferential boilerplate conclusion, insufficiency signaling).

## 6. Unsupported-claim detection

Definition (preserved): `assert_answer_grounded` raising AssertionError —
structural only (wrong version/order, altered passage/authority, unknown
chunk, wrong sufficiency label, inferential conclusion). A wrong
prediction is NOT an unsupported claim; a retrieval miss is NOT an
unsupported claim. E3 has no such mechanism (unsupported undefined in E3);
E4 flags `unsupported=True` on assertion failure and the verifier
independently rejects unlinked citations.

## 7. Prediction differences

NONE by construction: both call the identical shared
`EvidenceAugmentedPredictor` (frozen ckpt-6318, 512/50, mean-logit argmax)
on the identical input (facts + same selected passages). Prediction
equality is expected; prediction is secondary in RQ2.

## Controlled change / held constant / ablation validity

- Controlled change (A→D): post-selection provenance/citation/temporal
  verification + grounding assertion + structured rendering + fail-closed
  rejection. Nothing else.
- Held constant: 37 cases, facts text, split, preprocessing, BM25 index,
  checkpoint, seed, top-k, candidate retrieval, corpus, temporal definition.
- Genuine ablation: YES, but ONLY as A (E3: selection, no verification)
  vs D (full E4). Intermediate B/C (selection-only-provenance,
  citation-without-temporal) are not separable in this implementation —
  the verifier is an atomic contract — so inventing them would be
  relabeling, not science. RQ2 uses A and D only.
- Coupling limitation: because selection already embeds temporal+dedup
  gating, RQ2 cannot attribute protection to one sub-check from live data
  alone; the positive-control probes (mutated passage / mutated authority /
  backdated query year through the unchanged verifier) supply the
  per-check sensitivity evidence instead.
- Expected outcome: live-data ceiling (RQ1 already 150+35 checks passed,
  0 violations) is likely; discriminative power then rests on the probes
  plus the fail-closed property, reported honestly as such.
