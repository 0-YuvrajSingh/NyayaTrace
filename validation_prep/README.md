# Validation preparation workspace (NEW — does not modify frozen artifacts)

Purpose: hold *preparation-only* scaffolds for final validation. Nothing here
overwrites, regenerates, or reinterprets any frozen result.

Non-modification guard (binding on all future work):

- `answer_key/authority_answer_key.json` (30 evaluation + 3 dev_example, SHA
  `f4ccb0fa…00e81`) is IMMUTABLE. The 10-case extension lives in
  `answer_key/authority_answer_key_extension_10.json` (created only after human
  source verification) and is merged for analysis at read time only.
- `artifacts/e1_baseline_results.json`, `artifacts/e2_chunk_pool_results.json`,
  `artifacts/e3_e4_evidence_augmented_evaluation.json`,
  `config/reproducibility_freeze.json` (v4) are IMMUTABLE. Derived statistics
  (e.g. confidence intervals) are written under `validation_prep/` with
  `derived_from` provenance and never back-written into `artifacts/`.
- No retraining, no index rebuild, no retrieval-config change. Frozen version
  IDs (`week11-bm25-salient-terms-preranked-temporal-v3`,
  `tfidf-segment-salient-terms-v1`, `ildc-predecision-facts-v1`,
  `week9-citation-evidence-verifier-v2`,
  `week10-verified-explanation-renderer-v1`,
  `e3e4-evidence-augmented-inlegalbert-checkpoint6318-v1`) remain final.

Contents:

- `answer_key_extension/EXTENSION_PROTOCOL.md` — separate-round 10-case workflow.
- `answer_key_extension/extension_template.json` — empty 10-slot scaffold (no
  invented authorities; all annotation fields null).
- `rq3/RQ3_PACKET_SPEC.md` — independent blinded review spec (v3).
- `rq3/response_template_v3.json` — blank response scaffold (no synthetic ratings).
- `confidence_intervals/compute_cis.py` — stdlib-only read-only CI engine.
- `confidence_intervals/ci_results.json` — derived CI output (with provenance).
