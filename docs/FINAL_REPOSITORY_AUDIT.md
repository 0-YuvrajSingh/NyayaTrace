# FINAL REPOSITORY AUDIT — NyayaTrace
## Temporally Constrained and Provenance-Verified Legal Research over Indian Supreme Court Judgments

**Audit date (IST):** 2026-09-12
**Auditor:** Antigravity (final pre-submission audit pass)
**Source of truth:** Indian_Legal_XAI canonical specification (Document 3 Final)
**Commit audited:** ``d88c0bf`` ("Add RQ3 evaluation artifacts and results")
**Prior baseline commit:** ``2bd02b3`` ("Baseline: reproduce frozen v4 results")

---

## 1. Executive Verdict

**PASS WITH LIMITATIONS**

The repository is internally consistent, scope-conformant, methodologically faithful to the canonical specification, reproducible within documented environmental constraints, and free of unresolved submission blockers. All frozen answer-key hashes are confirmed. 75 applicable host-environment tests pass; 2 additional ML-stack tests are environment-limited because torch/transformers are unavailable in the host environment. The three canonical research questions are correctly stated with no RQ4 remnants in any submission artifact. E1-E4 match specification. Provenance, temporal, and citation integrity controls are verified. Known limitations are appropriately disclosed.

The working tree contains three legitimate modifications to submission artifacts (paper.md, paper.html, paper.pdf) representing a scope-alignment wording pass that removed a stale four-RQ structure and regenerated HTML/PDF accordingly. Three new documentation files in docs/ are untracked and not yet staged. Two test files requiring torch/transformers are environment-limited (not failures).

**There are zero submission blockers.**

---

## 2. Repository State

- Branch: main
- HEAD commit: d88c0bf (Add RQ3 evaluation artifacts and results)
- Prior commit: 2bd02b3 (Baseline: reproduce frozen v4 results)
- Working-tree modifications: M submission/paper.html, M submission/paper.md, M submission/paper.pdf
- Untracked files: docs/FINAL_PAPER_ARTIFACT_AUDIT.md, docs/FINAL_REPOSITORY_AUDIT.md, docs/FINAL_SCOPE_ALIGNMENT_REPORT.md
- Ignored artifacts: __pycache__/, *.pyc, .env, /retrieval/, large model caches (per .gitignore)

**Cleanup performed (Phase 12):**
- REMOVED: scripts/__pycache__/ -- Python bytecode; regenerated on import
- REMOVED: tests/__pycache__/ -- Python bytecode; regenerated on import
- REMOVED: src/legal_xai/__pycache__/ -- Python bytecode; regenerated on import
- REMOVED: .pytest_cache/ -- Pytest cache; regenerated on test run
Total: 42 .pyc files + 4 cache directories removed. No experiment/data/result/config/frozen artifact modified.

---

## 3. Scope Conformance: PASS

Repository correctly implements an Explainable Legal Research and Decision-Support Framework, not an autonomous judge or lawyer.

- Primary task (evidence retrieval + explainable case analysis): PRESENT in E3/E4
- Secondary task (historical outcome prediction): PRESENT; labeled secondary throughout
- Not autonomous judicial decision-making: CONFIRMED - fail-closed; human-review flag on all outputs
- Not production legal SaaS: CONFIRMED - static local demo; documented
- Not multilingual: CONFIRMED - English-only; multilingual in future work
- Not GraphRAG / graph database: CONFIRMED - 0 code hits
- Not multi-agent reasoning: CONFIRMED - 0 code hits
- Not large foundation-model leaderboard: CONFIRMED
- No autonomous lawyer/judge claim: CONFIRMED

---

## 4. RQ Conformance: PASS

Exactly three canonical RQs in submission/paper.md Section 5:

- RQ1: Does grounding an Indian legal AI workflow in retrieved legal evidence improve legal-research reliability and relevant-evidence retrieval compared with a facts-only legal-language baseline?
- RQ2: Does provenance-constrained evidence selection and citation verification reduce unsupported or unverifiable legal claims in the final output?
- RQ3: Can the proposed structured explanation format improve human-verifiable transparency without materially degrading prediction or retrieval performance?

RQ4 status: ABSENT from all submission artifacts. Zero "RQ4" occurrences in paper.md or paper.html.
Old stale labels (RQ1-Outcome baselines, RQ2-Evidence recovery, RQ3-Explanation format, RQ4-Evidence-augmented prediction) removed in scope-alignment pass documented in docs/FINAL_SCOPE_ALIGNMENT_REPORT.md.

RQ mapping: RQ1 -> E2-vs-E3 (37-case reference set) | RQ2 -> Condition A vs D + 111/111 probes | RQ3 -> 14-case blinded LLM evaluation
E1 role: Traditional predictive baseline only; explicitly stated not to answer RQ1.

---

## 5. E1-E4 Conformance: PASS

- E1: TF-IDF + LogReg, facts-only, C=10.0, seed 202605 -- config/e1_baseline.json consistent with artifacts/e1_baseline_results.json
- E2: InLegalBERT b5ecfed8ed6cf9d25a3cb8225a8c52f161f7401a; 512-token windows 50-overlap; mean-logit pooling; seed 202607; discarded 256-prefix retained transparently -- config/e2_chunk_pool.json consistent
- E3: Same E2 checkpoint at inference + BM25 FTS5 pre-rank temporal; top-100; top-5 source-diverse; salient query builder v1 -- config/evidence_selection.json consistent
- E4: E3 + citation_verifier.py (5-check chain) + renderer-v1; shared predictor identical to E3 -- config/citation_verification.json consistent; 0/185 verified items rejected on live data

E3/E4 comparison: identical checkpoint, input, seed, top-k, temporal policy, selected evidence. Controlled change = post-selection verification and rendering. No canonical E4-minus-E3 prediction-delta metric defined. Bundled-intervention caveat documented in paper Section 9.8.

---

## 6. Data / Answer Key / Freeze Integrity: PASS

Hash verification results:
- answer_key/authority_answer_key.json: expected f4ccb0fa8bfc11425988eb0b615b491c9908a97cb9d2c8a5343a14dae8600e81 -- MATCH
- answer_key/extension_v6/verified_7_case_extension.json: expected afa0329f49afc7041cc824bcbee0e4469097588b03bc3f9009b547bb2ff4495d -- MATCH

37-case reference set: 30 frozen (base key, byte-identical) + 7 additive (extension_v6). Assembly: read-time concatenation; both sources unmodified. Statement in manifest: "Additive extension only. No baseline frozen asset was modified."

Anti-leakage: Each case verified independently of system retrieval (independent_of_system_retrieval: true in every entry). Reference evidence predefined before final test evaluation. No retrospective construction from model outputs. Dev probe (9-case) and 30-case held-out are separate populations. Self-match floor calibrated from aligned/misaligned document-pair distribution (not retrieval results).

Content-alignment correction: 20/30 originally passed; 9 failed; 1 unresolved -- all 10 replaced with new content-aligned cases; final 30/30 direct-content passes confirmed.

---

## 7. Provenance / Citation Audit: PASS

Implementation chain verified (src/legal_xai/citation_verifier.py):
FINAL CITATION -> AUTHORITY IDENTITY CHECK -> DOCUMENT EXISTS -> PASSAGE EXISTS -> PASSAGE RETRIEVED FOR THIS QUERY -> TEMPORAL ELIGIBILITY CHECK -> PROVENANCE-VALID / REJECT (fail-closed)

Positive control probes (all on 37-case set):
- Passage mutation: 37/37 rejected
- Authority mutation: 37/37 rejected
- Temporal backdate: 37/37 rejected

Live-data results (185 displayed citations across 37 cases):
- Citation groundedness: 1.0 (185/185)
- Citation provenance validity: 1.0 (185/185)
- Temporal violation rate: 0.0 (0/185)
- Unsupported claim rate: 0.0 (0/37)
- E4 rejected items: 0

Minimum stored fields present: source_id, citation, decision_date, court, pdf/page/char locators, chunk_id, retrieval_rank, retrieval_run_id, temporal_status, query_case_id.

---

## 8. Temporal Audit: PASS WITH LIMITATIONS

Implementation: precedent_year < query_year (strict less-than, year-granular, applied BEFORE BM25 ranking and LIMIT 100).
Same-year sources: excluded as ambiguous.
Missing/unparseable dates: excluded.

Canonical spec says decision_date <= case_date. Implementation is stricter (same-year excluded). Deviation is:
- Conservative (fewer false positives)
- Documented in paper Section 13.6 ("Year-level temporal granularity")
- Technically justified: ILDC supplies only year-level identifiers

No false day-level ordering claims anywhere in paper, artifacts, or documentation. Wording consistent throughout.

---

## 9. RQ3 Audit: PASS

Counts: 14 cases, 4 evaluators (Gemini/Claude Sonnet 4.6/DeepSeek/GPT-5.6 Luna), 112 display observations (4x14x2), 56 forced preferences (4x14), 5 dimensions. All verified exact.

Evidence parity: same frozen verified evidence in both conditions; parity audit 7/7 (base). Condition mapping hidden during evaluation; applied post-rating; 0 mismatches on 112 rows.

Evaluation type correctly described as: exploratory (rq3_results.json title); LLM-based (rq3_report.md Section 1); non-human (paper Section 13.8 "not independent usability or legal-correctness evidence").

Absent claims verified: no human evaluation, no statistical significance, no causal evidence, no independent human study, no legal-correctness validation.

DeepSeek/GPT-5.6 Luna byte-identical outputs: disclosed in results notes; runs retained separately; NOT described as independent model families or independent human evaluators.

All reported numbers verified bit-exact against CSV artifacts:
- evidence_linkage: S 4.589286 / U 2.839286 / D +1.75
- citation_verifiability: S 4.696429 / U 3.696429 / D +1.0
- traceability: S 4.642857 / U 2.160714 / D +2.482143
- explanation_clarity: S 4.732143 / U 2.214286 / D +2.517857
- transparency_inspectability: S 4.642857 / U 2.660714 / D +1.982143
- overall: S 4.660714 / U 2.714286 / D +1.946429
- Preferences: 56/56 structured; 0 unstructured; 0 tie

---

## 10. Paper / HTML / PDF Consistency: PASS WITH LIMITATIONS

paper.md -> paper.html -> paper.pdf: all regenerated from same source in scope-alignment pass (documented in docs/FINAL_PAPER_ARTIFACT_AUDIT.md). HTML and PDF track current Markdown.

Critical wording checks in generated HTML:
- Zero "RQ4" occurrences: PASS
- Old "RQ1 - Outcome baselines" label absent: PASS
- Three canonical RQs with verbatim spec wording: PASS
- "no fourth research question" explicit sentence: PASS
- E1 contextual ("does not itself answer RQ1"): PASS
- LLM-exploratory non-human sentence: PASS
- Static-demo/efficiency/diagram limitation sentences: PASS

Numeric values spot-checked: E1 acc 0.6134/F1 0.6123, E2 acc 0.5968/F1 0.5924, E3/E4 acc 0.6667/F1 0.6032, R@5 12/30, R@100 15/30, 185/185 integrity checks -- all match authoritative JSON artifacts.

Residual limitation: PDF character-level content unverifiable locally (glyph-subset encoding). HTML structural verification confirmed (18 h2, 29 h3, 5 tables, 5 figures match paper.md). PDF valid PDF-1.4, 18 pages.

---

## 11. Claim-Safety Audit: PASS

Overclaiming term scan (submission artifacts and reports):
- "proves": 1 occurrence -- negation ("does not prove") -- SAFE
- "guarantees": 0 -- SAFE
- "legally correct"/"legal correctness": 2 -- both negations -- SAFE
- "autonomous": ~3 -- all negations -- SAFE
- "replaces lawyer"/"replaces judge": 0 -- SAFE
- "human evaluation": 2 -- both explicit negations -- SAFE
- "statistically significant": 0 -- SAFE
- "significant improvement": 0 -- SAFE
- "state-of-the-art": 0 -- SAFE
- "production-ready": 0 -- SAFE

Key separations confirmed:
- Prediction != legal correctness (paper Section 2 explicit)
- Provenance != substantive correctness (paper Section 10 explicit)
- Retrieval recall incomplete and prominently reported (15/30 absent at k=100)
- RQ3 described as exploratory observation, not causal proof
- N=30/37 results described as descriptive, not generalizable

---

## 12. Limitations / Disclosure Audit: PASS

All canonical and project-documented limitations are disclosed in paper Section 13 and supporting documentation:
Year-granular temporal rule; precedent-only corpus; ILDC/Supreme Court scope; English-only scope; prediction != legal correctness; provenance != substantive correctness; exploratory non-human RQ3; bundled E4 attribution; descriptive N=30/37; static local demo; efficiency metrics unreported; no standalone architecture diagram; semester-scale prototype; answer-key era concentration (43.3% 1980s); OCR repair quality; single expected authority per query; residual recovery gap (15/30 absent); DeepSeek/GPT-5.6 Luna byte-identical outputs; torch floating-point nondeterminism.

No new limitations invented. All disclosures present and accurate.

---

## 13. Reproducibility Audit: PASS WITH LIMITATIONS

14-item canonical freeze (config/reproducibility_freeze.json v4): All 14 items frozen and verified.
34/34 hashes confirmed in prior verification + clean replay.

No machine-specific paths, usernames, secrets, or API keys in tracked files:
- .env gitignored
- No absolute home directory paths in Python source
- No API keys in src/, scripts/, config/, artifacts/, or experiments/

All experiment scripts referenced in documentation exist. Known environment dependencies documented (PostgreSQL, local E2 checkpoint, eCourts PDFs, CUDA for training). Mutable-after-eval items disclosed (torch float tails, Docker image tags).

---

## 14. Test Results: PASS (2 environment-limited)

75 passed, 0 failed (Python 3.13.14, pytest 9.1.1)

Tests passing include:
- Citation verifier positive controls (altered passage, fabricated authority, temporal backdate, retrieval-run check, duplicate check): 18/18 PASS
- Temporal eligibility (earlier/same/later/missing/unparseable): 8/8 PASS
- Grounding assertions (fail-closed behavior): 8/8 PASS
- Alignment gate: 4/4 PASS
- Evidence pipeline (temporal pre-ranking): 4/4 PASS

Environment-limited (NOT code failures):
- tests/test_e2_chunk_pool_windows.py: ImportError: No module named 'transformers'
- tests/test_evidence_augmented_prediction.py: ModuleNotFoundError: No module named 'torch'
Both require full ML stack. Prior runs with complete environment passed per artifacts/week16_reproducibility_audit.md.

---

## 15. Blockers: NONE

Zero unresolved submission blockers. The one prior blocker (stale 4-RQ wording in paper.html) was resolved by regenerating paper.html and paper.pdf from the corrected paper.md source, documented in docs/FINAL_PAPER_ARTIFACT_AUDIT.md.

---

## 16. Final Recommended Submission State: READY

Pre-commit checklist:
1. git add docs/ (stage 3 untracked audit docs)
2. git add submission/paper.md submission/paper.html submission/paper.pdf (stage alignment + regeneration)
3. git diff --stat HEAD confirms only documentation wording changes; no frozen artifacts modified
4. Commit with clear message (e.g., "Final scope alignment, HTML/PDF regeneration, and repository audit")
5. Tag the commit (e.g., v5-final-submission)
6. Do NOT push until institutional submission requirements confirmed

Pre-commit sanity:
- pytest (excl. ML tests): 75 passed
- Answer-key hash check: both MATCH
- git diff --stat HEAD: only paper.md, paper.html, paper.pdf in tracked files
