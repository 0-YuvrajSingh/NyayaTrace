# Freeze report — extension v6: 37-case reference-evidence set (30 frozen + 7 verified)

## 1. Purpose

Promote the 7 VERIFIED expansion candidates into an immutable, versioned
reference-evidence extension. Additive only: the original 30-case key is
canonical history and is not rewritten, regenerated, or reformatted.

## 2. Baseline frozen reference set

- Original case count = 30 (`answer_key/authority_answer_key.json`,
  SHA `f4ccb0fa8bfc11425988eb0b615b491c9908a97cb9d2c8a5343a14dae8600e81`).
- Manifest: `answer_key/authority_answer_key_manifest.md`
  (SHA `302182ec58741230…`, 5,316 bytes).

## 3. Verification input

- Source: `answer_key/expansion_v5/verification/verification_results.json`
  (packet `expansion-v5-candidates-v1`; report + decisions + passage audits
  v1/v2/v3 as supporting evidence).
- Status counts: 7 VERIFIED + 3 NEEDS_REVIEW (asserted programmatically
  before promotion; all VERIFIED records have all nine gates PASS).

## 4. Promotion (exactly 7)

1990_234, 1990_256, 1990_324, 1991_136, 1991_87, 1992_286, 1993_90 —
full verification evidence preserved verbatim per record (identities,
citations, excerpts, passages with locators, gates, normalizations with
original forms, OCR verbatim). No field invented, weakened, or strengthened.

## 5. Exclusion (exactly 3 NEEDS_REVIEW, not promoted)

1991_198 (background_reference listing), 1993_89 (unresolved court
treatment), 1990_188 (party_relied_on_only). Exclusion is not falsification;
these remain packet candidates pending any future authorized review.

## 6. Result

Logical reference set = 37 cases (30 frozen + 7 extension). Extension file
holds only the 7 new cases plus base-set pointer (no 30-case duplication):
`answer_key/extension_v6/verified_7_case_extension.json`
(SHA `afa0329f49afc704…`).

## 7. Frozen file integrity (before/after identical)

answer_key/authority_answer_key.json: `f4ccb0fa…00e81` before and after.
authority_answer_key_manifest.md: `302182ec…` before and after.

## 8. Frozen asset integrity

Byte identity re-verified after extension build: ILDC train
(`0d878a…`), validation (`2140d5…`), test (`10cddb…`); BM25
(`3187f7…`); E2 checkpoint (`924a5b…`); freeze record present and
untouched. No regeneration, rebuild, retrain, or data alteration.

## 9. Duplicate/count checks

A: no duplicate IDs in extension. B: no overlap with frozen 30.
C: no prohibited duplicate authority entries. D: no NEEDS_REVIEW promoted.
E: extension count exactly 7. F: combined count exactly 37. All PASS.

## 10. Required-field checks

All 7 records carry the 13 required items (query/case identity, query
citation, authority identity, authority citation, relationship, exact
authority passage, source/provenance ID, passage ID/locator, query year,
authority date/year, temporal result, verification status, all nine gates).
No missing values; nothing fabricated.

## 11. Temporal/provenance checks

Frozen year-granular rule applied as recorded (all authority_year <
query_year; query side year-only, no invented dates). Provenance fields
(source_id, chunk locators, paths, dates) preserved per record. All seven
remain VERIFIED. Temporal policy unchanged.

## 12. Test-suite results

Full available suite executed after extension creation (see final report).

## 13. Files created/modified

Created (new dir only): `answer_key/extension_v6/verified_7_case_extension.json`,
`answer_key/extension_v6/extension_manifest.json`,
`answer_key/extension_v6/FREEZE_REPORT.md`. Modified: none.

## 14–16. Explicit statements

- No RQ1/RQ2/RQ3 experiment was run in this task.
- No frozen baseline artifact was modified (hashes §7–8).
- This is an additive extension, not a rewrite of the original reference key,
  which remains the canonical 30-case historical artifact.

Terminology: cases are source-verified, evidence-verified,
provenance-traceable, temporally eligible, reference-evidence verified.
No claim of legal correctness or retrieval completeness is made.

Generation: `freeze_build.py` + `freeze_manifest.py` (deterministic JSON:
sort_keys, indent 2, trailing newline, UTF-8; stdlib only, no new
dependency). Baseline commit `2bd02b3`, tag `v4-baseline-reproduced`
(unchanged; nothing committed).
