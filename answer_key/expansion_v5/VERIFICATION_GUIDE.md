# Verification Guide — expansion_v5 candidates (human gate before any promotion)

No candidate in `candidates.json` is verified. Every entry is NEEDS_REVIEW.
Promotion into an official 40-case key requires ALL steps below, performed by
a human against external sources. Retrieval output is never sufficient basis.

## Step 0 — Confirm frozen key untouched

`answer_key/authority_answer_key.json` (30 evaluation + 3 dev_example) must
remain byte-identical (SHA `f4ccb0fa…00e81`). New entries go only to a future
`answer_key/authority_answer_key_extension_10.json` per
`validation_prep/answer_key_extension/EXTENSION_PROTOCOL.md`.

## Step 1 — Query judgment identification (external source)

For each `candidate_case_id`: locate the judgment outside this project (live
court portal / SCR host preferred; eCourts mirror scraped from `scr.sci.gov.in`
accepted). `own_mirror_ecourts_id` (present for 5/10) is a starting pointer,
not proof — run the content-alignment audit (title/party + ≥100 shared
six-token fingerprints) before trusting the mapping. Record `query_source_url`.

## Step 2 — Authority relationship (the core judgment call)

For each `proposed_authorities[]` entry: read the source judgment and decide
whether the cited authority was genuinely applied/relied_on/distinguished/
quoted_for_principle (schema `allowed_relationships`). A bare mention string
(`query_excerpt`) is NOT enough. Discard passing mentions; keep at most the
authorities the judgment actually uses. Record exactly one primary authority
per case unless two are independently justified (never pad for metrics).

## Step 3 — Authority source + passage

For each kept authority: open the authority source document (`authority_path`
locates the eCourts file; prefer the live portal for the final locator),
select the verbatim applied passage, record page/paragraph locator
(`source_locator`), reporter citation, `verification_source_url`,
`verified_on` date, and `verification_method` (`native-text`/`OCR-repaired`
per the Week 3 audit; residual low-quality exclusions are ineligible).

## Step 4 — Temporal re-check (year-granular)

Query side is ILDC year-only: recompute `authority_year < query_year` from the
recorded exact `authority_decision_date`. Same-year or missing-date
authorities are evaluation-ineligible (explicit ambiguity note required).

## Step 5 — Duplicate re-check

Confirm the kept authority is not the query case itself and not an audited
near-duplicate (`duplicate_pair_with_query` flags are mechanical pre-checks,
all False here — re-confirm after any source substitution). Any substitution
restarts Steps 1–4 for that case.

## Step 6 — Mechanical gates + freeze addendum

Run `python scripts/check_answer_key_candidate.py --case-id <ID>` (must
APPROVE), then `python scripts/validate_authority_answer_key.py` on
frozen-30 + extension-10. Record the extension file SHA in a NEW freeze
addendum (never edit v4). Report 30-case and 40-case metrics side by side.

## Rejection rules (record reason in the packet)

REJECT on: no applied authority found; only SCC/AIR mentions resolvable with
no corpus source; same-year-only authority; failed content alignment;
quality-excluded source; any field requiring invention. Rejections are data.
