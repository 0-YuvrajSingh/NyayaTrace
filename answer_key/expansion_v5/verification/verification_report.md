# Verification report — expansion_v5 repository-side verification v1

"0 candidates are VERIFIED unless every required gate below has been independently satisfied."

## 1. Methodology

Packet: `answer_key/expansion_v5/candidates.json` (10 NEEDS_REVIEW, unmodified).
For each candidate: ILDC test-split record retrieval (Step 1); citation
located in actual query text with treatment classification (Step 2);
authority resolved in eCourts metadata + chunks with real locators (Step 3);
relationship classified ONLY from query-court language (Step 4); real
authority-side passage with chunk/page locator, never constructed (Step 5);
alignment via record+citation+metadata+(mirror where present), never bare
identifier equality (Step 6); frozen rule authority_year < query_year,
year-granular on the query side (Step 7); crosswalk + self-match safeguards,
no new policy (Step 8); external review kept supplementary with unavailable
URLs recorded as unavailable (Step 9). Legal correctness, provenance
validity, and retrieval relevance kept strictly separate throughout.

## 2. Gate definitions

Nine gates, each PASS / FAIL / NEEDS_REVIEW: query_identity,
query_citation, authority_identity, relationship, authority_passage,
content_alignment, temporal, duplicate, provenance. VERIFIED requires all
nine PASS. Allowed relationships: applied / relied_on / distinguished /
quoted_for_principle / party_relied_on_only / background_reference /
unresolved. Mention/listing/counsel-reliance are never upgraded.

## 3. Candidate-by-candidate results

See `verification_decisions.md` for full records and `verification_results.json`
for machine-readable gates. Headline per candidate:

- 1991_87 Khardah: court holds ratio "of no assistance" → distinguished → VERIFIED.
- 1991_198 Manjusri: "see A, B, C and D" background list → background_reference → NEEDS_REVIEW.
- 1991_136 Patankar: counsel analogy rejected ("we do not agree") → distinguished → VERIFIED.
- 1990_234 Balmadies: court uses Balmadies observations to decide Art.31A point → relied_on → VERIFIED.
- 1990_324 Prithvi Raj Taneja: court adopts small-plot view and applies ("accordingly ... fixed") → relied_on → VERIFIED (Pridviraj normalization documented).
- 1992_286 Bandhua Mukti Morcha: court-introduced verbatim Art.21 quotation, externally corroborated → quoted_for_principle → VERIFIED.
- 1993_89 Dhillon: only counsel exchange evidenced; court holding unknown → unresolved → NEEDS_REVIEW.
- 1993_90 DCM: court invokes s.58A validation as supporting precedent → relied_on → VERIFIED (DCM normalization documented).
- 1990_188 Firestone: reliance "on behalf of the workmen" only → party_relied_on_only → NEEDS_REVIEW.
- 1990_256 Chandra Deo: court states holding as governing → relied_on → VERIFIED (prokash = corpus spelling).

## 4. Summary table

| Candidate | Query identity | Authority | Relationship | Query citation | Authority passage | Temporal | Duplicate | Alignment | Final |
|---|---|---|---|---|---|---|---|---|---|
| 1991_87 | PASS | PASS | distinguished/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |
| 1991_198 | PASS | PASS | background_reference/FAIL | PASS | NEEDS_REVIEW | PASS | PASS | NEEDS_REVIEW | NEEDS_REVIEW |
| 1991_136 | PASS | PASS | distinguished/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |
| 1990_234 | PASS | PASS | relied_on/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |
| 1990_324 | PASS | PASS | relied_on/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |
| 1992_286 | PASS | PASS | quoted_for_principle/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |
| 1993_89 | PASS | PASS | unresolved/NEEDS_REVIEW | PASS | NEEDS_REVIEW | PASS | PASS | NEEDS_REVIEW | NEEDS_REVIEW |
| 1993_90 | PASS | PASS | relied_on/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |
| 1990_188 | PASS | PASS | party_relied_on_only/FAIL | PASS | NEEDS_REVIEW | PASS | PASS | NEEDS_REVIEW | NEEDS_REVIEW |
| 1990_256 | PASS | PASS | relied_on/PASS | PASS | PASS | PASS | PASS | PASS | VERIFIED |

## 5. Unresolved issues

- 1991_198: listing-only; would need evidence of court adoption (none found) — likely unpromotable.
- 1993_89: court holding on Dhillon not established in examined passages; full-text human read could resolve either way.
- 1990_188: court adoption of Firestone rule not evidenced; human full-text read could resolve either way.
- Normalizations recorded (original + normalized + reason): "Pridviraj" → Prithvi Raj Taneja (1990_324); "dcm limited v. u. o.l" → Delhi Cloth (1993_90); "prokash"/"prakash" alias noted, no change (1990_256).
- External URLs: all unavailable (recorded as such); external evidence used as supplementary only, never decisive.
- No query-record per-record hash exists in-repo (aggregate only); recorded honestly.

## 6. Integrity checks

- Frozen 30-case key, ILDC splits, corpus, BM25 index, checkpoint, baseline artifacts, frozen configs: verified unchanged (see final integrity run).
- No candidate beyond the original 10 added; packet file unmodified.
- No VERIFIED status without all nine gates passing (machine-checked).
- Test suite executed (see integrity run). No commit/push performed.

## 7. Final count

VERIFIED: 7 (1991_87, 1991_136, 1990_234, 1990_324, 1992_286, 1993_90, 1990_256).
NEEDS_REVIEW: 3 (1991_198, 1993_89, 1990_188).
No 40-case key created — promotion is a separate, explicitly authorized step.
