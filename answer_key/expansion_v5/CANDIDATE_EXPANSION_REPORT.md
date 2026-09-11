# Candidate Expansion Report — 30 → 40 preparation (packet, NOT a key)

Frozen key preserved: `answer_key/authority_answer_key.json` unmodified
(30 evaluation + 3 dev_example). No 40-case key created. No RQ1/RQ2,
no retrieval comparisons, no ablations, no v4 changes.

## 1. Numbers

- Candidates found (mechanical SCR-resolution pool): 113 / 1,487 scanned
- Packet (strongest 10 by era-weighted signal): 10
- Provisionally suitable for human review: 10
- Source-verified: **0**
- Requiring human verification: **10**
- Rejected in this phase: 0 from packet (1,374 non-pool cases out of scope,
  not rejected; 14 facts-ineligible excluded mechanically)

## 2. Candidate-to-authority mappings (primary = most-mentioned resolved)

| Candidate | Q-year | Primary proposed authority | Authority date | Mentions | Mirror |
|---|---|---|---|---|---|
| 1991_87 | 1991 | 1963 INSC 127, [1964] 3 S.C.R. 506 | 02-05-1963 | 1 (+8 more) | 1991 INSC 70 |
| 1991_198 | 1991 | 1977 INSC 49 | 09-02-1977 | 1 (+7 more) | none |
| 1991_136 | 1991 | 1960 INSC 145 | 08-09-1960 | 2 (+6 more) | 1991 INSC 102 |
| 1990_234 | 1990 | 1972 INSC 115 | 19-04-1972 | 1 (+5 more) | 1990 INSC 210 |
| 1990_324 | 1990 | 1977 INSC 16 | 18-01-1977 | 1 (+5 more) | none |
| 1992_286 | 1992 | 1983 INSC 203 | 16-12-1983 | 1 (+5 more) | 1992 INSC 186 |
| 1993_89 | 1993 | 1971 INSC 289 | 21-10-1971 | 1 (+5 more) | none |
| 1993_90 | 1993 | 1983 INSC 79 | 21-07-1983 | 2 (+4 more) | none |
| 1990_188 | 1990 | 1976 INSC 26 | 13-02-1976 | 1 (+4 more) | none |
| 1990_256 | 1990 | 1963 INSC 9 | 22-01-1963 | 1 (+3 more) | 1990 INSC 240 |

Full per-authority detail (all proposed authorities, excerpts, flags) is in
`candidates.json`. Every relationship = UNKNOWN; every authority passage =
UNKNOWN — deliberately.

## 3. Temporal checks

All proposed authorities satisfy `authority_year < query_year` mechanically
(query side ILDC year-only → explicitly **year-granular**; authority side
exact eCourts dates shown above). Same-year/post-date mentions were
pre-filtered out of the packet. Human must re-verify from recorded exact
dates at promotion (VERIFICATION_GUIDE.md Step 4).

## 4. Duplicate checks

Self-match (cited doc == query's own mirror): excluded mechanically during
mining; 0 self-matches in packet. Crosswalk duplicate-pair flags: all False
across all proposed authorities. Citation ambiguity: all matches unique
(`ambiguous_matches: 1` throughout). Content-alignment audit NOT yet done —
required human step (packet `duplicate_note`).

## 5. Rejection / unresolved reasons

- No packet candidate rejected; pool method fixed two miner bugs honestly
  (INSC-style citations absent from ILDC text; regex year-capture fix).
- Known limits: SCC/AIR mentions (e.g. 1991_87: 11 SCC + 2 AIR) are
  UNRESOLVED mechanically — human SCC→SCR concordance may add or replace
  authorities. Unresolved SCR keys listed per candidate (e.g. 1991_87: 5).
- Era gap UNRESOLVED: all 10 are 1990s. Post-2000 non-frozen cases (19)
  carry ~zero SCR-form citations (18 with 0 hits; 2002_171 with 1
  unresolvable hit), so SCR-resolution cannot supply 2000s/2010s cases.
  The 1980s skew of the frozen key is therefore not corrected by this
  packet — 2000s/2010s expansion needs SCC/AIR-concordance or portal-led
  sourcing (recommended next action #3).

## 6. Recommended next action (ordered)

1. Human review of the 10 packet cases per VERIFICATION_GUIDE.md
   (relationship + passage + source URL/date/method + alignment audit).
2. Promote only passing cases to `authority_answer_key_extension_10.json`
   (separate file; frozen 30 untouched), then validator + freeze addendum.
3. For era balance: run a portal-led (not retrieval-led) sourcing round for
   2000s/2010s test cases with SCC/AIR→corpus concordance; do not lower the
   alignment or source-quality floors to fill the decade gap.
4. Do NOT finalize any 40-case key, run RQ1/RQ2, or compare retrieval until
   Steps 1–2 complete.
