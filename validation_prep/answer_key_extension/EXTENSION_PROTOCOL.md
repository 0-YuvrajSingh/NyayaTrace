# 40-case answer-key expansion protocol (SEPARATE ROUND — frozen 30 untouched)

Status: WORKFLOW ONLY. No new cases verified; no authorities recorded here.
Target file (to be created after human verification, never before):
`answer_key/authority_answer_key_extension_10.json`

## 1. Invariants

1. `answer_key/authority_answer_key.json` (30 `evaluation` + 3 `dev_example`)
   is never edited, reordered, or re-serialized by this workflow.
2. New entries live ONLY in the extension file and carry `"status": "evaluation"`,
   `"round": "extension-10"`. Analysis code reads frozen-30 + extension-10 and
   concatenates at read time.
3. Schema is `config/authority_answer_key_schema.json`
   (`week7-authority-key-v3`). All `required_entry_fields` apply unchanged,
   including `independent_of_system_retrieval: true` and the prohibited source
   rule (no citation ever returned/ranked/suggested by project retrieval).
4. No authority, date, citation, locator, or annotation is invented, inferred
   from retrieval output, or copied from model text. Every field is transcribed
   by a human from the external source.

## 2. Candidate selection (before any source work)

1. Gate every candidate with the frozen checker (read-only against test split):
   `python scripts/check_answer_key_candidate.py --case-id <ILDC_ID>`
   REJECTED ids must not enter source verification.
2. Exclude the 30 frozen evaluation IDs and the `2019_890` dev IDs
   (enumerate programmatically from `answer_key/authority_answer_key.json`;
   do not hard-code the list here so the frozen file stays single-source).
3. Era targeting (per `answer_key/authority_answer_key_manifest.md` watch):
   prioritize post-1990s/2000s/2010s ILDC test IDs to dilute the 1980s
   over-representation (13/30). Record offered-but-unverifiable IDs in the
   round log with reasons (no aligned source / quality-excluded / same-year
   only) — non-resolution is data, not failure.
4. Stop at 10 verified entries. Surplus verified cases (if any) go to a
   backlog list, never into the frozen 30.

## 3. Per-case human verification (mirrors Weeks 7–10 pacing record)

For each candidate, a human verifier records: query judgment identified from
an EXTERNAL source (live portal / SCR host preferred; eCourts mirror scraped
from `scr.sci.gov.in` accepted with `source`, `verification_method`
(`native-text`|`OCR-repaired` per Week 3 audit), `not`); exactly one authority
explicitly cited/applied with page/paragraph locator (`relationship` ∈
`allowed_relationships`); direct public source URL + `verified_on` date;
temporal note (authority must satisfy `precedent_year < query_year`; same-year
authorities need explicit ambiguity note and are evaluation-ineligible without
one); content-alignment evidence (title/party + ≥100 shared six-token
fingerprints against the eCourts source text — reuse the audit method, do not
lower the floor).

## 4. Validation gate (all must pass before the extension file is accepted)

1. `python scripts/validate_authority_answer_key.py` (frozen validator) passes
   on frozen-30 + extension-10 concatenated (schema, test-split membership,
   mirror method/audit agreement, temporal eligibility).
2. Alignment re-audit on the 10 new query-source mappings: 10/10 pass or the
   failing case is replaced (same rule as the 2026-08-30 re-resolution).
3. Spot retrieval check is READ-ONLY and INFORMATIONAL (as in Week 9): record
   ranks, never tune retrieval, never drop a case for being unretrieved.

## 5. Freeze update

On acceptance: record the extension file's SHA-256/bytes in a NEW freeze
addendum (`config/reproducibility_freeze_addendum_40.json`, new file; v4
untouched), keep the 30-case evaluation reproducible standalone, and report
30-case and 40-case metrics side by side (never overwrite 30-case numbers).
