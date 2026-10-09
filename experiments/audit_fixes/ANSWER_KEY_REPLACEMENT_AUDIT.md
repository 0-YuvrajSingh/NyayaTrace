# Answer Key Replacement Audit

## Independence of System Retrieval
The property `independent_of_system_retrieval` is a self-declared flag and cannot serve as evidence of true independence. To verify independence, we must rely on git commit order or execution logs to prove that replacements occurred before any retrieval results for those cases were seen.

According to `answer_key/authority_answer_key.json`, the 10 changed cases (9 replaced + `2013_35`) have a `verified_on` date of `2026-08-30`. However, the earliest git commit in this repository is `2026-09-12T00:02:32+05:30` ("Baseline: reproduce frozen v4 results"). No dated evidence exists before it, and `verified_on` is a self-declared field. Therefore, the ordering cannot be definitively proven from the logs.

**Overall Verdict**: NOT PROVABLE

## Replacement Case Analysis
According to `artifacts/answer_key_reresolution.md`, the header row of the resolution table is:
`| Flagged case | Old invalid query source | Resolution | Final query case / source | Direct phrases | Title/party | Authority and parallel check |`

The columns distinguish between **case replacement** (where both the query case and authority are new, providing a fresh test case) versus **source re-resolution** (where the query case remains the same but a corrected authority source is identified, as in `2013_35`).

1. **`2013_30`**: (Line 19) `| 2013_30 | 2013_1_243_266 | Source absent after phrase/title search; replacement | 1977_99 / 1977_3_372_388 | ...` (Replaced by `1977_99`)
2. **`2013_57`**: (Line 21) `| 2013_57 | 2013_3_359_375 | Fresh source 2013_1_130_139 had 1,232 direct phrases but failed title/party; replacement | 1980_217 / 1980_3_1243_1252 | ...` (Replaced by `1980_217`)
3. **`2013_101`**: (Line 22) `| 2013_101 | 2013_3_392_415 | Source absent after phrase/title search; replacement | 1980_133 / 1980_3_884_892 | ...` (Replaced by `1980_133`)
4. **`2013_121`**: (Line 23) `| 2013_121 | unresolved / 2013_2_116_125 | Fresh source 2013_4_753_766 had 1,690 direct phrases but failed title/party; replacement | 1978_33 / 1978_3_131_146 | ...` (Replaced by `1978_33`)
5. **`2008_516`**: (Line 24) `| 2008_516 | 2008_6_1009_1039 | Source absent after phrase/title search; replacement | 1981_187 / 1981_3_839_848 | ...` (Replaced by `1981_187`)
6. **`2002_171`**: (Line 25) `| 2002_171 | 2002_2_808_824 | Fresh source 2002_1_775_785 had 1,556 direct phrases but failed title/party; replacement | 1980_222 / 1980_3_1127_1142 | ...` (Replaced by `1980_222`)
7. **`2013_95`**: (Line 26) `| 2013_95 | 2013_1_984_995 | Source absent after phrase/title search; replacement | 1977_145 / 1977_3_428_436 | ...` (Replaced by `1977_145`)
8. **`2017_14`**: (Line 27) `| 2017_14 | 2017_1_330_365 | Fresh source 2017_1_265_277 had 1,839 direct phrases but failed title/party; replacement | 1981_55 / 1981_2_910_929 | ...` (Replaced by `1981_55`)
9. **`2001_414`**: (Line 28) `| 2001_414 | S_2001_2_463_472 | Source absent after phrase/title search; replacement | 1980_105 / 1980_3_44_70 | ...` (Replaced by `1980_105`)
10. **`2013_35`**: (Line 20) `| 2013_35 | 2013_1_267_294 | Corrected accepted-crosswalk match | 2013_35 / 2013_1_327_335 | ...` (The query case ID remained unchanged, but the underlying query source was corrected from `2013_1_267_294` to `2013_1_327_335` after source-ID and title/date reconciliation. The authority was NOT changed.)

**Temporal Rule Causation:** None of the 9 replacements were caused by the temporal rule. All 9 were replaced due to content mismatch caused by identifier collisions between ILDC and eCourts.

## Presence in Prediction Cross-Reference
The 9 old replaced IDs continue to appear in `artifacts/week12_prediction_cross_reference.json` under keys such as `['full_test_n1503_E1_E2_outcome_disagreement', 'both_correct', 'case_ids']`. This is because they remain part of the full 1517-case frozen ILDC test split. The models evaluated them as part of the full test set. 

(Note: The cross-reference uses `n1503` rather than 1517 because 14 cases from the 1517-case test split were dropped due to being ineligible/too short for windowing, leaving exactly 1,503 eligible cases evaluated by both models. This is also why E1 and E2 confusion matrices sum to 1,503.)

## Year Distribution of Query Cases
- **Old Query Cases (Replaced):** 2001 (1), 2002 (1), 2008 (1), 2013 (5), 2017 (1). Distribution heavily skews toward the 2000s and 2010s.
- **New Query Cases (Replacements):** 1977 (2), 1978 (1), 1980 (4), 1981 (2). Distribution is strictly restricted to 1977-1981.

## Verdicts per Case
- **2013_30 (New: 1977_99)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2013_57 (New: 1980_217)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2013_101 (New: 1980_133)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2013_121 (New: 1978_33)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2008_516 (New: 1981_187)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2002_171 (New: 1980_222)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2013_95 (New: 1977_145)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2017_14 (New: 1981_55)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2001_414 (New: 1980_105)**: NOT PROVABLE (no dated evidence before 2026-09-12)
- **2013_35 (Corrected)**: NOT PROVABLE (no dated evidence before 2026-09-12)
