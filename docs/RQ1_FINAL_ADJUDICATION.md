# RQ1 Final Scientific Adjudication

Date: 2026-10-08. This is a verification record. No manuscript, code, experiment output or frozen artifact was modified.
It supersedes the RQ1 sections of `docs/GROUND_TRUTH_ADJUDICATION.md` and `docs/SCOPE_AND_MANUSCRIPT_DIAGNOSIS.md` (the latter removed in the 2026-10-09 cleanup).

## 0. How the ground truth was established

The PostgreSQL provenance store was unavailable (Docker not running, no `.env`). Both RQ1 conditions were therefore **rebuilt read-only** from frozen inputs:
- Index: `retrieval/bm25.sqlite`, opened `mode=ro`; byte-identical to the freeze.
- Corpus: the local cleaned eCourts corpus.
- Code: the project's own functions, `fts_query`, `exclude_query_duplicate`, `assess_temporal_eligibility`, `select_diverse_evidence`, `temporal_preranked_bm25_sql` and `_candidate_matches_expected`.
- Control SQL: the same FTS5 statement without the year predicate, as preserved in `experiments/audit_fixes/scripts/bm25_ranking_probe.py:15-18`.

Scripts live in the session scratchpad, outside the repository: `rq1_reconstruct.py` and `bm25_identity.py`.

**Validation against the frozen artifacts** (`artifacts/week11_initial_evaluation.json` = control, `artifacts/week11_temporal_prerank_evaluation.json` = temporal): **30/30 cases match on all 7 checks.** The checks are facts SHA-256; candidate count after safety filters (both conditions); the **exact ordered selected chunk IDs** (both conditions); and the raw-top-5 / top-100 / selected flags (both conditions). The reconstruction is exact.

**BM25 identity test** (`bm25_identity.py`): for all 30 queries, filtering the unfiltered ranking to `decision_year < Y_q` reproduces the pre-ranked top-100 **with identical chunk IDs, identical order, and maximum score difference 0.0**. There were no ties at the cutoff and no query had insufficient depth.

## 1. Per-case table (reconstructed and validated)

"Raw rank" means the best rank of any expected-authority chunk in the returned top-100 list, the quantity the code calls `rank`. "Elig. pos." means the authority's position among the control's eligible candidates.

| Case | Control raw rank | Control raw ≤5 | Control selected | Control elig. pos. | Temporal raw rank | Temporal selected | Control top-100 | Temporal top-100 |
|---|---:|:-:|:-:|---:|---:|:-:|:-:|:-:|
| 1971_295 | — | N | N | — | — | N | N | N |
| 1974_36 | — | N | N | — | — | N | N | N |
| 1977_145 | — | N | N | — | — | N | N | N |
| 1977_99 | 2 | Y | Y | 1 | 1 | Y | Y | Y |
| 1978_33 | — | N | N | — | — | N | N | N |
| 1980_105 | 42 | N | **Y** | 1 | 1 | Y | Y | Y |
| 1980_133 | 48 | N | N | 15 | 15 | N | Y | Y |
| 1980_217 | — | N | N | — | — | N | N | N |
| 1980_222 | 6 | N | **Y** | 1 | 1 | Y | Y | Y |
| 1981_187 | — | N | N | — | 2 | **Y** | N | **Y** |
| 1981_55 | — | N | N | — | 28 | N | N | **Y** |
| 1982_29 | 14 | N | **Y** | 1 | 1 | Y | Y | Y |
| 1984_136 | — | N | N | — | — | N | N | N |
| 1985_40 | — | N | N | — | 78 | N | N | **Y** |
| 1986_176 | 11 | N | **Y** | 2 | 2 | Y | Y | Y |
| 1986_378 | — | N | N | — | — | N | N | N |
| 1986_397 | — | N | N | — | — | N | N | N |
| 1988_96 | 13 | N | **Y** | 1 | 1 | Y | Y | Y |
| 1992_84 | — | N | N | — | — | N | N | N |
| 1993_185 | — | N | N | — | — | N | N | N |
| 1994_632 | — | N | N | — | — | N | N | N |
| 1995_322 | 5 | Y | Y | 1 | 1 | Y | Y | Y |
| 1995_375 | 4 | Y | Y | 2 | 2 | Y | Y | Y |
| 1995_403 | — | N | N | — | — | N | N | N |
| 1995_412 | — | N | N | — | — | N | N | N |
| 1995_425 | 1 | Y | Y | 1 | 1 | Y | Y | Y |
| 1997_792 | — | N | N | — | — | N | N | N |
| 2002_944 | 6 | N | **Y** | 1 | 1 | Y | Y | Y |
| 2008_1629 | 1 | Y | Y | 1 | 1 | Y | Y | Y |
| 2013_35 | — | N | N | — | — | N | N | N |

Expected authorities (citation, title, date) are in `answer_key/authority_answer_key.json`. In every recovered case, **control eligible position = temporal raw rank**, so order is preserved. The control displayed only 135 citations, because 7 cases had fewer than five eligible sources in the top 100: 1977_99 (2), 1980_105 (2), 1981_187 (1), 1981_55 (3), 1985_40 (4), 1986_378 (4), 1995_403 (4).

## 2. Metrics

| Metric | Control (post-ranking filter) | Temporal (pre-ranking) | Δ |
|---|---:|---:|---:|
| A/C. Raw rank ≤5 (code's `recall_at_5`) | 5/30 (0.1667) | 12/30 (0.4000) | +7 |
| **B/D. Among the five selected sources (paper Table I definition)** | **11/30 (0.3667)** | **12/30 (0.4000)** | **+1** (1981_187) |
| E. Recall@100 | 12/30 (0.4000) | 15/30 (0.5000) | +3 (1981_187, 1981_55, 1985_40) |
| Candidates after safety filters | 2,743 (764 eligible, 1,712 later-year, 267 same-year) | 3,000 (all eligible) | |
| Displayed citations | 135 | 150 | +15 |

**Current Table III and Abstract** report **row A/C for Recall@5** under a label whose definition (Table I) is row B/D. The two coincide only in the temporal condition. The six cases where they diverge in the control (1980_105, 1980_222, 1982_29, 1986_176, 1988_96, 2002_944) already **displayed** the expected authority. In those cases later judgments occupied raw ranks 1–5 but were never displayable.

## 3. The four stages, precisely

1. **Raw top-5** is the first five rows of the BM25 list returned by SQLite. In the control this list includes later-year and same-year chunks.
2. **Post-ranking temporal filtering (control)** takes `LIMIT 100` over all years. The filter is then applied by `assess_temporal_eligibility` labels, and the selector skips non-eligible items (`evidence_pipeline.py:108`). Display is therefore temporally clean, but ineligible rows consume the 100 slots.
3. **Five-source selection** walks candidates by (−BM25, rank) and takes up to five eligible candidates, at most one per source (`evidence_pipeline.py:93-114`). This is what the user sees and what Table I's Recall@5 defines.
4. **Pre-ranking temporal filtering (final)** puts `decision_year < Y_q` inside the FTS candidate relation, before `ORDER BY ... LIMIT 100` (`evidence_pipeline.py:34-40`). All 100 slots then go to eligible material.

## 4. Monotonicity: guaranteed by the implementation

All six premises hold:
1. Same index and statistics: one FTS5 table, and `bm25()` uses whole-table statistics. Verified empirically: score difference 0.0.
2. Eligible chunks' scores are unchanged: verified, 0.0.
3. The only difference in the candidate set is the removal of `decision_year ≥ Y_q`: verified, with identical IDs and order on 30/30.
4. Every expected authority is eligible: all 30 have `temporal_status: eligible_by_year`, and every recovered authority carries `eligible` status in both runs.
5. Order among eligible chunks is unchanged: verified (eligible position = pre-ranked rank).
6. Downstream processing is identical: the same `exclude_query_duplicate` (depends only on query and source) and the same `select_diverse_evidence`.

**Proof.** Let E be the eligible non-duplicate candidates in BM25 order.
- The control's eligible top-100 is a prefix of E, because each eligible row in the global top 100 has fewer than 100 rows of any kind above it.
- The temporal top-100 is the first 100 of E, so it contains that prefix.
- *k = 100:* any expected authority in the control's top 100 is in the prefix, and therefore in the temporal top 100.
- *Five-source selection:* the selector walks E in the same order in both conditions and stops at five distinct sources. The control's selection is the same walk truncated at the end of the prefix. If the prefix holds five or more distinct sources, the two selections are identical. Otherwise the temporal selection extends the control's.

Neither metric can decrease. The only theoretical exception, ties at the LIMIT boundary, was checked and did not occur.

**Required statement, which the code supports exactly:** "The observed increase is not an unbiased test of whether temporal filtering improves retrieval quality. The experiment instead measures how much recovery is gained when temporally ineligible candidates are prevented from occupying ranking positions."

## 5. Chronology of test-informed decisions

Git history begins 2026-09-12 (`2bd02b3`, bulk import), so it cannot establish anything earlier. The times below come from artifact-internal records.

| # | Event | Date/time | Data | Purpose | Inspected before final config? | Evidence |
|---|---|---|---|---|---|---|
| 1 | Week-9 answer-key spot check | undated, before 08-29 | 10 Base-30 cases (1982_29, 1985_40, 1986_397, 1988_96, 1992_84, 1994_632, 1995_403, 1995_412, 1995_425, 2002_944) | Check retrieval and selection on new key entries | Yes | `artifacts/week9_answer_key_spot_checks.json`; manifest "Week 9 expansion" |
| 2 | Query-builder freeze regression | undated (Week 9) | **6 Base-30 cases**: 1986_397, 1988_96, 1995_412, 1995_425, 2002_944, 2008_1629 | "results determine … the final query-construction freeze decision"; rule: salient non-worsening on all six → `adopt_salient_tfidf` | **Yes: configuration decision** | `artifacts/week9_final_freeze_regression.json` (`purpose`, `freeze_recommendation`) |
| 3 | Rank reconciliation | 2026-08-29 16:42–17:20 UTC | 3 Base-30 cases (2008_1629, 1995_425, 2002_944) | Explain rank differences; "no retrieval tuning or configuration change" | Yes (diagnostic) | `artifacts/week10_rank_reconciliation.json` (`created_at_utc`, `scope`) |
| 4 | Self-match repair, then query-builder regression rerun | undated (Week 10) | Same 6 Base-30 cases | "Required one-time rerun … results determine the final query-construction freeze decision" | **Yes: configuration decision** | `artifacts/week10_post_selfmatch_freeze_regression.json`; `week10_reproducibility_freeze.md:9` |
| 5 | Dev probe v2 built (9 train/val cases) | 2026-08-30 | Train/validation | Replaces invalidated v1 | — | `answer_key/dev_retrieval_probe.json` (`verified_on`, `supersedes`) |
| 6 | Alignment audit, re-resolution, 9 replacements | 2026-08-30 | Answer key | Identity correction (content/corpus gates, not retrieval) | — | manifest §"Content-alignment…", §"Content-driven re-resolution" |
| 7 | Evaluation round frozen | 2026-08-30T10:44:42Z | — | — | — | `config/week11_evaluation_round.json` `frozen_at_utc` |
| 8 | **Post-ranking evaluation on Base-30** | after #7, undated | All 30 | First full test scoring | **Yes** | `artifacts/week11_initial_evaluation.json` (round v1) |
| 9 | **Pre-ranking run and comparison on Base-30; adoption** | after #8, undated | All 30, including per-case raw-candidate logs (2013_35: 79 eligible; 1980_105: 3) | "Adopt pre-ranking temporal filtering" | **Yes: configuration decision** | `artifacts/week11_temporal_preranking_investigation.md` ("Decision"); `week10_reproducibility_freeze.md:11` ("It is adopted as the final configuration") |
| 10 | Dev-probe consistency check 6/9 → 7/9 | after #9 | Dev 9 | "run only for consistency after the real-cohort comparison" | No (post-selection) | `week11_temporal_preranking_investigation.md:42` |
| 11 | Final results | 2026-09-01T11:39:44Z | Base-30 | Final scoring (same run as #9) | — | `week11_evaluation_round.json` `finalized_at_utc` |
| 12 | E3/E4 prediction revision | 2026-09-06 | Base-30 | Adds prediction; retrieval unchanged | — | `reproducibility_freeze.json` `revision_history` |
| 13 | Extension-7 verified and frozen | 2026-09-11; frozen 19:24:09Z | 7 new test cases | Additive reference set | No (built after the freeze) | `expansion_v5/verification/verification_results.json`; `extension_v6/extension_manifest.json` |
| 14 | RQ1/RQ2 37-case runs | 2026-09-11 20:02Z / 20:59Z | 30 + 7 | Final configuration only (no control arm) | — | `experiments/rq1|rq2/*_run_manifest.json` |
| 15 | Manuscript scoring | through 2026-10-05 | Frozen outputs | No new retrieval | — | git `cf1ca2a` |

**Answers.**
- **A.** Yes. Pre-ranking was selected using Base-30 (#9). The query builder was also frozen using 6 Base-30 cases (#2, #4).
- **B.** Inspected: aggregate R@5 (raw-rank), R@100, selected and retrieved-not-selected counts, regressions, candidate status counts, and per-case raw-candidate composition (#9). For the query builder, the ranks and status of the expected authority for the 6 controls (#2, #4).
- **C.** Yes. The final 12/30 and 15/30 come from the same run that decided the adoption (#9 = #11).
- **D.** No. The 9-case dev probe was independent of the test set (train/validation), but for pre-ranking it was evaluated only after the test-informed decision.
- **E.** Yes. Extension-7 did not exist until 10 days after the configuration was finalized. Its cases were selected mechanically from SCR citations resolved in the query judgments, with "no retrieval comparisons" (`expansion_v5/CANDIDATE_EXPANSION_REPORT.md` header; `VERIFICATION_GUIDE.md:5`: "Retrieval output is never sufficient basis").
- **F.** Partly. It is a genuinely untouched check of the final configuration's absolute recovery: R@5 (selected = raw) 0/7, R@100 5/7 (`experiments/rq1/RQ1_REPORT.md`). It has **no control arm**, so it cannot confirm the comparison. It is small (n = 7) and era-concentrated (1990–1993), and every case has the authority mentioned in the query judgment by construction. It was not pre-registered as confirmatory.

## 6. Scientific status

- **RQ1 is a development-informed systems characterisation.** Its direction is structurally guaranteed and its configuration was chosen on the same cases. It is not a confirmatory test.
- **No new held-out run is required.** A held-out comparison cannot test a direction that is fixed by construction. It could only re-estimate the magnitude of displacement on new cases, which the paper does not need to claim.
- The control Recall@5 had to be reanalysed. The correct value, 11/30, is already stored in the frozen artifact (`expected_authority_selected`, `authority_consistent_recall` 0.366667), so no computation beyond reading it is needed.

## 7. Integrity and other items (unchanged from the prior adjudication; re-confirmed)

- **150/150:**
  - It is an observed cross-store consistency result on the evaluated pipeline.
  - It is largely forced by the extract-only renderer and the eligible-only selector.
  - **H2 was not tested.** There is no unconstrained arm, and the RQ2 "A" condition produces identical output.
- **Tamper probes:**
  - 90/90 on Base-30 (passage, authority and backdate, 30 each), and 111/111 over 37 cases including the extension.
  - They are function-level positive controls on real outputs (`experiments/rq2/run_rq2_37.py:144-161`), not an evaluation outcome.
- **Tests:** 81 test functions. 75 were executed and passed (`docs/FINAL_REPOSITORY_AUDIT.md:225`; re-run 2026-10-08). 6 PyTorch/Transformers-dependent tests were never executed (`FINAL_REPOSITORY_AUDIT.md:235-236`; `replay/pytest.log`). No record shows 81/81. **Addendum 2026-10-09:** all 81 tests, including the six PyTorch/Transformers tests, were executed and passed in the `nyayatrace-e2:frozen` Docker image (torch 2.5.1+cu124, transformers 4.46.3; `experiments/audit_fixes/replay/logs/pytest_docker_2026-10-09.log`). The paper now reports 81/81 (75 host + 6 Docker).
- **Freeze:** 39 paths = 29 byte-identical, 8 differing only in line endings, 2 with content changes. The paper's 30/22/8 has no source.
