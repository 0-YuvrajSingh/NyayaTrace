# Ground-Truth Adjudication of the First-Pass Diagnosis

Date: 2026-10-08. Scope: verification only. No manuscript, experiment, or frozen artifact was modified.
Supersedes the corresponding items in `docs/SCOPE_AND_MANUSCRIPT_DIAGNOSIS.md` (removed in the 2026-10-09 cleanup).

> **Cleanup note (2026-10-09).** Files cited below as evidence that were later removed: `all_40_corrections.txt` (subset of the retained `all_40_corrections_full.txt`), `build_canonical.py`, `update_docx_canonical.py`, `scratch/test_checks.py` (untracked one-off scripts that wrote or enforced the false 30/22/8 sentence), `paper_master_final.tex` / root `research_paper.tex` (byte-identical copies of the canonical `submission/research_paper.tex`), and `docs/PHASE2_9_FINAL_RELEASE_AUDIT.md`, `experiments/audit_fixes/replay/final_reference_resolution.md` (tracked; recoverable from git at `cf1ca2a`). See `docs/REPOSITORY_CLEANUP_2026-10-09.md`.
Manuscript: `submission/research_paper.tex` (byte-identical to root `paper_master_final.tex` / `research_paper.tex`).

**Evidence limits.** Git history begins at `2bd02b3` (2026-09-12, "Baseline: reproduce frozen v4 results"). Weeks 1–11 therefore have no commit-level chronology. Their chronology below comes from timestamps and hashes recorded inside the artifacts, not from file modification times. The PostgreSQL provenance store was not running, so per-candidate BM25 scores were not re-queried.

---

## A. Freeze audit

**Recomputed now** (all `path`+`sha256` records in `config/reproducibility_freeze.json`): 43 hash records over **39 unique paths**. The four repeated paths carry identical hashes.

| Class (mutually exclusive, tested in this order) | Count | Paths |
|---|---:|---|
| Byte-identical | **29** | incl. ILDC parquets, BM25 SQLite, checkpoint, answer key, all frozen code |
| Identical after converting the current LF file to CRLF | **8** | `ecourts_corpus_identity.json`, `bm25_index.json`, `e1_baseline_results.json`, `e2_correction_manifest.json`, `e3_e4_evidence_augmented_evaluation.json`, `e3_e4_prediction_error_analysis.json`, `week10_dev_probe_selfmatch_recheck.json`, `week11_temporal_prerank_evaluation.json` |
| Content differs | **2** | `corpus/dataset_manifest.md` (15,337 B now vs 15,355 B frozen); `artifacts/week10_post_selfmatch_freeze_regression.json` (8,530 B frozen vs 8,532 B after CRLF conversion) |

1. **What the audits counted.** `docs/freeze_drift_audit.md` (2026-09-21) covers the same 39 paths and reports 28 / 1 (CRLF→LF) / 10. The "1" was `docker/e2.Dockerfile`, which became byte-exact after the `.gitattributes` fix (RR-02). It now reports **29 / 0 / 10** under the same classification. My extra test (current LF → CRLF) splits those 10 into 8 that differ only in line endings and 2 with real content changes.
2. **Why the paper says 30 / 22 / 8.** Commit `cf1ca2a` (2026-10-05) replaced "39 entries: 28 byte-exact, one line-ending-normalized, 10 metadata-differing" with "30 entries: 22 byte-exact, 8 byte-drift". The source was an external instruction file, `all_40_corrections.txt` item 4: "Keep the 30-entry freeze-audit result exactly as: 22 byte-exact … 8 …". **No audit artifact, script output, or manifest anywhere in the repository produces 30, 22, or 8.**
3. **Are 39/28/1/10 and 30/22/8 the same audit?** 39/28/1/10 is the actual audit. 30/22/8 is not an audit result.
4. **Are the categories mutually exclusive?** The hash classes are (byte-exact, line-ending-equivalent, differs). "Metadata-only" is not a hash class. It is a cause annotation in `freeze_drift_audit.md`, and **for the 8 line-ending files it is wrong.** For example, the doc says `e1_baseline_results.json` changed Python 3.11.9→3.13.14 and sklearn 1.9.0→1.9.1. The current file still records 3.11.9 / 1.9.0 and equals the frozen bytes after CRLF conversion. The doc's UUID and float-tail explanations for the E3/E4 and week-11 JSONs are likewise unsupported, because those files are content-identical to the frozen versions. For the 2 content-changed files, the frozen bytes are not retained in git, so the nature of the change cannot be verified beyond its size.
5. **Correct sentence.** "Of the 39 paths hashed in the freeze record, 29 are byte-identical, 8 differ only in line endings, and 2 development-record files differ in content." None of the 10 contains a headline result except the line-ending-only ones, and those are content-identical.
6. **`validate_final.py:20-21` enforces the false sentence.** `scratch/test_checks.py`, `build_canonical.py` and `update_docx_canonical.py` do too. `docs/freeze_drift_audit.md` needs its cause column corrected.

## B. RQ1 temporal pre-ranking

**Implementation facts.**
- Final SQL: `src/legal_xai/evidence_pipeline.py:34-40`, `WHERE chunks_fts MATCH ? AND decision_year < ? ORDER BY bm25 LIMIT 100`.
- The baseline is **not "unfiltered BM25"**. It is the superseded **post-ranking filter** run (`artifacts/week11_initial_evaluation.json`, config `week10-bm25-salient-terms-selfmatch-coverage-v2`). It takes the raw top-100, labels each candidate with a temporal status, and the selector (`select_diverse_evidence`, line 108) displays **only eligible** candidates.
- Both runs use the same 30 case IDs, the same salient-term query builder, the same self-match rule and the same answer key.

**The metric definition actually computed** (`scripts/run_week11_initial_evaluation.py:160-163`): `recall_at_5 = expected authority has a chunk with raw retrieval rank ≤ 5`. This is a rank-based measure over the returned list, which in the baseline includes later-year and same-year chunks. **Paper Table I instead defines Recall@5 as "among the five selected sources".**

**Per-case comparison (verified from both artifacts):**

| Measure | Post-ranking baseline | Pre-ranking | Δ | Cases gained | Lost |
|---|---:|---:|---:|---|---:|
| Raw-rank ≤5 (code's "Recall@5") | 5/30 | 12/30 | +7 | 1980_105, 1980_222, 1981_187, 1982_29, 1986_176, 1988_96, 2002_944 | 0 |
| **Selected among the 5 displayed (paper's Table I definition)** | **11/30** | **12/30** | **+1** | 1981_187 | 0 |
| Recall@100 | 12/30 | 15/30 | +3 | 1981_187, 1981_55, 1985_40 | 0 |
| Displayed citations | 135 | 150 | +15 | — | — |

In the pre-ranked run, raw-rank ≤5 and selected are the same 12 cases, so the two definitions coincide there. They do **not** coincide in the baseline. In 6 baseline cases the expected authority was already displayed, but later judgments occupied raw ranks 1–5.

**Monotonicity: weak dominance is guaranteed by construction.**
1. *Identical scores.* FTS5 `bm25()` uses whole-table statistics (row count, per-term document frequency). A `WHERE`/`JOIN` predicate does not change them, as the docstring at line 30 also states. The scores were not re-queried (the DB was offline). The observed 0 regressions, and every dev-probe rank staying the same or improving, are consistent with this.
2. *Only change.* The eligibility predicate moves from after `LIMIT` to before it. Same-year and missing-date rows (NULL `<` Y is not true) are removed in both conditions before display.
3. *Expected authorities are eligible.* By construction, each answer-key authority is an earlier authority cited by the query judgment (`temporal_status` in the answer key). Both runs report 0 temporal violations.
4. *Rank.* An eligible chunk's pre-ranked rank is 1 + (number of eligible chunks scoring above it), which is ≤ its raw rank. It cannot fall.
5. *Selection.* The eligible candidates in the baseline top-100 are exactly the prefix of the pre-ranked eligible list. The selector walks that list in the same order. Its output is therefore identical when the prefix has ≥5 distinct sources, and a superset-compatible extension otherwise. No counterexample is possible.
6. *Self-match and duplicates.* `exclude_query_duplicate` depends only on the query and the candidate source, never on the condition.
7. *Other behaviour.* The only theoretical exception is ties at the `LIMIT` boundary, where SQLite's order within ties is unspecified. No regression was observed.

**Consequence.** The direction of the gain is guaranteed, so "does pre-ranking improve recovery?" cannot come out the other way. The experiment validly measures **how much retrieval capacity temporally ineligible judgments displaced**: 1,712 later-year and 267 same-year candidates among the 2,743 logged baseline candidates, and 3 authorities pushed below the top-100. The user-visible display-level effect is +1 case at k=5 and +3 at k=100. **RQ1 should be reframed as a controlled characterisation of displacement, not as a causal "does it improve?" hypothesis**, and Recall@5 must be reported consistently with its stated definition.

**Chronology problem (discovered in this pass).** `artifacts/week11_temporal_preranking_investigation.md` records that the pre-ranking change was **adopted after comparing both configurations on the frozen 30 test cases**. The dev probe (6/9→7/9) was "run only for consistency after the real-cohort comparison". The paper (§VIII-E) instead says "The final configuration came from three development steps on a nine-case probe (0/9, 3/9, 6/9, then 7/9 at k=100) … the pattern held on the base set". That misstates the order. Mitigating facts: the change has no tunable parameter, it cannot lower recovery (see above), and both runs are preserved. Spec §28 nevertheless forbids adopting settings after inspecting final test results, so this must be disclosed.

## C. 150/150 grounding and provenance

| Layer | What it guarantees or checks | Evidence |
|---|---|---|
| Architecture | The renderer copies `text` of the selected candidates verbatim. It refuses ineligible or duplicate evidence. The conclusion mode is `evidence_bound_no_inference`. | `grounded_answer.py:112-124`, `config/grounded_answer.json` (`controlled_extract_only`) |
| Grounding audit | `assert_answer_grounded` re-compares the passage text and 7 metadata fields with the selected objects. Unknown chunks or authorities are rejected. | `grounded_answer.py:127-180` |
| E4 verifier | It re-derives each citation from PostgreSQL `corpus_chunks` and the `retrieval_results` of that run. It checks metadata, case/citation/date/court, query duplicate, temporal eligibility (a separate date-parsing path from the SQLite `decision_year`) and run membership. | `citation_verifier.py:113-174`, `run_grounded_answer_pipeline.py:21` |
| Observed (Base-30) | 150/150 passed, 0 temporal violations, 0 unsupported, 0 rejected. E3 and E4 inputs are identical. | `week11_temporal_prerank_evaluation.json` |
| Corrupted inputs | See D. | |
| Unconstrained arm | **None.** RQ2's "A" condition (`experiments/rq2`) is the same extract-only pipeline with checks skipped, and its output is identical to D. No unconstrained generation or selection condition exists. | `RQ2_REPORT.md` |

**Verdict: both.** The sentence "all 150 displayed base citations passed …" is a valid observed result. Specifically, it is a cross-store consistency check: a SQLite/PostgreSQL mismatch, a date-parsing disagreement or a run-logging defect would have surfaced. It is also a near-invariant of the extract-only design.
**The paper may NOT claim:** reduced hallucination or unsupported claims relative to any baseline; improvement over an unconstrained system; that H2 was tested; or that 1.00 demonstrates reliability gains. **H2 was not tested.** The paper's current RQ2 wording ("keep … within the checks") is compatible with this. A single sentence stating the by-construction status and the absence of a control arm is sufficient.

## D. E4 negative testing

**Unit tests** (synthetic fixtures; all included in the 75 that passed today):
- `test_citation_verifier.py`: missing corpus chunk; altered passage; fabricated case-name field; tampered citation metadata; citation not in run; later year; same year; audited near-duplicate; authority without linked evidence.
- `test_grounded_answer.py`: altered passage and unknown authority; unsupported conclusion; non-eligible evidence; out-of-order structure.
- `test_temporal.py`: earlier, same, later, missing and unparseable dates.

**Positive-control probes on real E4 outputs** (`experiments/rq2/run_rq2_37.py:144-161`; per-case CSV verified). These are function-level calls to `verify_answer_citations` on each case's live rendered answer:

| Probe | What is altered | Base-30 | Extension-7 | Total |
|---|---|---:|---:|---:|
| Passage mutation | first evidence passage + " [MUTATED]" | 30/30 | 7/7 | 37/37 |
| Authority mutation | first authority citation → "FABRICATED 9999 XYZ 0" | 30/30 | 7/7 | 37/37 |
| Temporal backdate | query year set before the earliest evidence year | 30/30 | 7/7 | 37/37 |

"111/111 rejected" is arithmetically correct (3 × 37), but it pools the post-freeze extension cases. For Base-30 the correct figure is **90/90 (30 per probe type)**. These are probe results, not "E4 achieved 111/111" on the evaluation. Each probe mutates only the first item, and "rejected" means at least one check failed.

**Coverage by category.** Passage alteration: unit + probe. Wrong authority/citation: unit + probe. Wrong source: unit (unlinked evidence / unknown chunk). **Wrong date (decision_date metadata tamper): checked in code (`citation_verifier.py:160-162`), no dedicated test.** Future source: unit + probe. Same-year: unit. Missing corpus item: unit. Out-of-run: unit. Query duplicate: unit.

**Distinction.** Unit tests show that each rejection rule works on synthetic inputs. The probes show that the verifier rejects corrupted versions of the actual evaluated outputs. The Base-30 evaluation shows that the uncorrupted outputs pass. None of the three shows improvement over an alternative system.

## E. RQ labels

The narrowing is intentional and documented: paper §III-A states that the broader specification covers RQ3 and that it is deferred. However, "RQ1"/"RQ2" carry different content from canonical RQ1/RQ2. Canonical RQ1 is grounding vs a facts-only legal-language baseline; paper RQ1 is pre-ranking vs post-ranking filtering. Placing them next to "(RQ3)" implies the labels are shared. **Least disruptive correct solution (option 1):** keep the paper's questions, add one clause saying they are paper-specific questions derived from the project's RQ1/RQ2, and rephrase RQ1 as a characterisation (see B). Canonical RQ1's facts-only comparison is already present for prediction (21/30 vs 20/30). A rename to Q1/Q2 is optional.

## F. Temporal rule

- **Implementation:** SQL `decision_year < Y_q` (pre-rank). The Python verifier uses `assess_temporal_eligibility`: year parsed from the exact eCourts date, `<` eligible, `==` `AMBIGUOUS_EXCLUDED`, `>` `INELIGIBLE`, missing or unparseable `EXCLUDED_MISSING_METADATA` (`temporal.py:56-97`). SQL NULLs also fail the predicate.
- **Why it differs:** ILDC exposes only the year (`config/datasets.json` `date_resolution: year_only`; `reproducibility_freeze.json:50` `known_limitation`).
- **Known before evaluation?** The rule is in the frozen configs, and the week-11 investigation states it was "retained without modification". Git cannot date it, because history starts after the evaluation.
- **Paper:** it documents the year rule, the same-year and missing-date exclusions, and the recall cost (§III, Table I, §X). It does not mention that the project's date-level rule (`decision_date ≤ case_date`) is looser. Because the paper never states the canonical rule, this is a should-fix clarification, not a factual error. The deviation is recorded in the freeze record.
- **"Temporal existence" (Table I)** is defined as "has a parseable exact decision date". That describes metadata availability, not the canonical "exists in the corpus at or before the relevant time". Should-fix.

## G. Controlled generation

1. **There is no generation component.** No causal LM, generation API or generative call exists in `src`, `scripts`, `config` or `demo/ml-service`. The feasibility check loaded only `InLegalBERT` and `legal-bert-small` (`artifacts/model-feasibility.json`).
2. `controlled_extract_only` is final (`config/grounded_answer.json`, frozen in `reproducibility_freeze.json`).
3. and 4. There is no evidence that generation was ever implemented or tested. The pre-2026-09-12 history is not in git.
5. and 6. It is not recorded as a deviation. `experiments/SCOPE_CONFORMANCE_AUDIT.md:35` classifies the extract-only renderer as "IMPLEMENTED (stricter than required)".
7. The paper's Introduction is accurate ("we do not test a generative system"). §III-A ("The broader project specification also covers controlled generation … RQ3 is deferred") implies that a generation component exists and was only not evaluated. **Report that the output layer is an extract-only renderer and that no generation component was built.** The spec's "where feasible" clause makes this a defensible design choice.

## H. Answer-key chronology (artifact-internal evidence)

| Step | Evidence |
|---|---|
| Week 9: 30-case key, including 10 cases added; retrieval spot check on the 10 new cases (2 selected, 3 retrieved-not-selected, 5 absent) | `authority_answer_key_manifest.md` "Week 9 expansion", `artifacts/week9_answer_key_spot_checks.json` |
| 2026-08-30: 3 of 8 dev spot reads mismatched → alignment audit of all 30 mappings: 20 pass / 9 fail / 1 unresolved | manifest "Content-alignment correction audit — 2026-08-30" |
| 2026-08-30: re-resolution: 1 relinked (2013_35), 9 replaced (4 failed title/party identity, 5 absent from the corpus). The era mix shifted (2000s 5→2, 2010s 7→1). | manifest; `artifacts/answer_key_reresolution.md` |
| 2026-08-30T10:44:42Z: evaluation round frozen (`week11_evaluation_round.json`) | `frozen_at_utc` |
| Post-ranking baseline scored on the corrected 30 (round v1) | `week11_initial_evaluation.json`; same 30 IDs as the final run (verified) |
| Pre-ranking adopted after the 30-case comparison; dev check afterwards | `week11_temporal_preranking_investigation.md` |
| 2026-09-01T11:39:44Z: final results | `final_results.finalized_at_utc` |

**Verdict.** "The answer key, including the replacement cases, was fixed before retrieval results were scored" is literally true for both reported scoring runs. Development spot checks had, however, observed retrieval results on superseded entries. The documented replacement reasons are alignment and corpus gates, not retrieval outcomes. **Safe wording:** "The answer key, including the replacement cases, was fixed before the reported retrieval evaluations were run; earlier development spot checks on superseded entries contribute to no reported metric." The real chronology issue is the configuration adoption in B.

## I. Query-leakage audit (independently recomputed)

Inputs: the frozen facts rule applied to `single_test.parquet`. **All 30 recomputed `facts_sha256` values match the frozen evaluation.** Columns:
- **Loose:** any non-generic authority-title token in the facts (the repo's audit definition; repo artifact = 18/30, my rerun = 19/30, with minor ignore-list differences).
- **Strict:** the petitioner-side party name appears as a phrase, or the reporter citation appears (14/30; includes generic hits such as "bank" and "assam", so it is an upper bound).
- **Salient:** a token appears among the 32 query terms.

| Case | Loose | Strict | Salient | R@100 | Selected | Rank |
|---|:-:|:-:|:-:|:-:|:-:|---|
| 1971_295 | Y | Y | N | N | N | — |
| 1974_36 | N | N | N | N | N | — |
| 1977_145 | Y | Y | N | N | N | — |
| 1977_99 | Y | Y | N | Y | Y | ≤5 |
| 1978_33 | N | N | N | N | N | — |
| 1980_105 | Y | N | N | Y | Y | ≤5 |
| 1980_133 | Y | Y | N | Y | N | 15 |
| 1980_217 | Y | N | N | N | N | — |
| 1980_222 | Y | Y | N | Y | Y | ≤5 |
| 1981_187 | Y | Y | N | Y | Y | ≤5 |
| 1981_55 | Y | Y | N | Y | N | 28 |
| 1982_29 | Y | Y* | N | Y | Y | ≤5 |
| 1984_136 | N | N | N | N | N | — |
| 1985_40 | Y | Y | N | Y | N | 78 |
| 1986_176 | Y | Y | N | Y | Y | ≤5 |
| 1986_378 | Y | N | N | N | N | — |
| 1986_397 | N | N | N | N | N | — |
| 1988_96 | Y | N | N | Y | Y | ≤5 |
| 1992_84 | Y | N | N | N | N | — |
| 1993_185 | Y | Y (citation) | N | N | N | — |
| 1994_632 | N | N | N | N | N | — |
| 1995_322 | N | N | N | Y | Y | ≤5 |
| 1995_375 | N | N | N | Y | Y | ≤5 |
| 1995_403 | N | N | N | N | N | — |
| 1995_412 | N | N | N | N | N | — |
| 1995_425 | Y | Y* | N | Y | Y | ≤5 |
| 1997_792 | Y | Y | N | N | N | — |
| 2002_944 | N | N | N | Y | Y | ≤5 |
| 2008_1629 | Y | Y | **Y** | Y | Y | ≤5 |
| 2013_35 | N | N | N | N | N | — |

\* generic token ("bank", "assam"). "≤5": in the final run, every selected authority also has raw rank ≤5 (verified equal sets).

**Interpretation.** Authority tokens reach the BM25 query in 1/30 cases, so direct query→answer string matching is negligible. That matches the paper. Mentions in the facts text are **normal legal citation**: the answer key records an earlier authority that the query judgment itself relied on, and the facts-only cut keeps the narrative that discusses it. This is not contamination of the evaluation target. Recovery is nonetheless concentrated in those cases: R@100 is 12/19 when the facts mention the authority (loose) versus 3/11 when they do not (Fisher exact p = 0.13, n = 30, descriptive). Recall@k therefore partly measures retrieval of authorities that the query text already discusses. This qualifies generalisation to unmentioned authorities. It does not invalidate the numbers. The paper's "18" and "1" are reproducible under the repo's definition, but "18" depends on that definition (14–19).

## J. E1 / E2 training data

Verified from the result artifacts:
- E1 selects C on validation (C = 10.0, at the edge of the grid), refits on **5,020 + 983 = 6,003** eligible documents, and tests once.
- E2 trains on **5,020** documents (33,702 windows). Validation (983) is used only for checkpoint selection (`checkpoint-6318`, validation accuracy 0.612411). It tests once.

E1 therefore sees 983 (19.6%) more labelled documents, and the validation split is label-balanced (491/492) while train is 62/38. The paper states both procedures separately but never names the asymmetry, even though it interprets E1 > E2 (non-significant). **Disclosure wording (supported):** "E1 is refit on training plus validation data (6,003 documents), whereas E2 is trained on the 5,020 training documents and uses validation only for checkpoint selection; the comparison therefore favours E1 in labelled-data exposure."

## K. Test count

- 81 `def test_` in `tests/`: 75 that need no torch, plus 6 that do (`test_e2_chunk_pool_windows.py` 2, `test_evidence_augmented_prediction.py` 4).
- Recorded executions: `docs/FINAL_REPOSITORY_AUDIT.md:225` "75 passed, 0 failed", with the torch files failing to import (lines 235–236). `replay/pytest.log` (2026-09-28): collection interrupted, 5 errors. `replay/pytest_fastapi.log`: demo ML service 2 passed / 4 failed (a separate suite).
- **Re-executed today** in an isolated venv (Python 3.14, pytest 9.1.1, pyarrow 25.0.1, scikit-learn 1.9.1; these are not the pinned versions): **75 passed; the 6 torch/transformers tests were not collected.**
- **No record anywhere shows the 6 passing.** "The implementation passes 81 tests" is unsupported. Correct: "75 of 81 unit tests were executed and passed; the 6 tests requiring PyTorch/Transformers were not executed in the audit environment." The paper's list of rejection behaviours exercised by unit tests is accurate. **Addendum 2026-10-09:** all 81 tests, including the six PyTorch/Transformers tests, were executed and passed in the `nyayatrace-e2:frozen` Docker image (torch 2.5.1+cu124, transformers 4.46.3; `experiments/audit_fixes/replay/logs/pytest_docker_2026-10-09.log`). The paper now reports 81/81 (75 host + 6 Docker).

## L. Literature and references

1. **"None address corpus-level record matching or exact citation provenance verification."** As scoped to [4]–[6], probably true. As a field-level claim it is unsupported, and the Related Work omits Indian legal retrieval work: the FIRE AILA tracks (2019–2021; 2019 confirmed to exist; I recall precedent and statute retrieval tasks) and IL-TUR (ACL 2024; I recall a prior-case-retrieval task, but my fetch could not confirm the task list). **Verify both before citing.**
2. **[6] Shukla et al.** The abstract confirms evaluation by law practitioners and states that "it is an open question on how best to evaluate legal case document summarization systems". It does not, from the abstract, establish that "legal documents require expert review over document-level metrics". Partial support; soften.
3. **[3] 2026 INSC 668.** The case, citation, date (2 July 2026), Civil Appeal No. 11950/2025, and the setting-aside of NCLT/NCLAT orders for non-existent or misattributed AI-generated citations are corroborated by secondary sources. The count "6 citations: 3 non-existent, 3 with non-existent paragraphs" and the phrasing "relevance, currency, authority, and applicability" attributed to it were **not verifiable** from the sources I could reach. Check them against the judgment PDF. **Addendum 2026-10-09:** checked against the judgment PDF itself (sci.gov.in, 11 pages, para 15): three citations are non-existent (ICICI Bank, V.S. Dempo, Sarbjit Singh); two are correct citations with non-existent paragraphs (Everest Kento, Canara Bank); one ("SBI v. Shree Ram Urban", 2020 SCC OnLine SC 341) is a wrong citation of an existing judgment (footnote 6: *M. Subramaniam v. S. Janaki*) with a non-existent paragraph. The paper now uses this breakdown, citing the judgment [3]. Para 7 supports the misconduct/serious-lapse sentence in Section XI.
4. **2026 references.**
   - [11] CaseFacts: verified (ACL 2026, `2026.acl-long.785`, arXiv 2601.17230; authors match; covers temporal validity and overruling). Pages not verified.
   - [13]: verified (arXiv 2605.25920, Wei Fan et al., LegalSearch-R1).
   - [14]: verified (arXiv 2608.09393, Cymbler, Guez and Fabre; also listed at ICML 2026).
   - [15]: title, journal, vol. 40, article number and DOI were verified by the repo's 2026-09-29 audit from the publisher record (my fetch got 403). The paper's description, "TaxFlow filters for validity in Indian tax-law question answering", is **not verified**. Only a related-work snippet in arXiv 2608.06828 mentions a "TaxFlow" hybrid RAG framework. Either verify the content or drop the descriptive claim.

## M. Anonymity

No target venue is recorded (`docs/PHASE2_9_FINAL_RELEASE_AUDIT.md:104`: "No target venue specified"). The PDF carries five author names, the AKGEC affiliation, institutional emails, and `github.com/0-YuvrajSingh/NyayaTrace`. The repository's commit author identity is personal. **Flag only:** this is fine for single-blind review and must be anonymised if the venue is double-blind.

---

## N. Adjudication table

| Issue | Previous diagnosis | Verified? | Evidence | Scientific consequence | Required paper action |
|---|---|---|---|---|---|
| 1 Freeze audit | 39: 28/1/10; paper's 30/22/8 wrong | **Corrected.** Paper wrong. Today: 39 = 29 exact / 8 line-ending-only / 2 content | Recomputed hashes; `cf1ca2a` diff; `all_40_corrections.txt` #4 | Reproducibility claim is factually false. The drift doc's cause column is also wrong. | Replace the sentence; fix `validate_final.py` and the drift doc |
| 2 RQ1 monotonicity | Direction guaranteed | **Confirmed, and worse.** Baseline is post-ranking, not unfiltered; R@5 baseline 5/30 uses raw rank, while the paper's definition gives 11/30 | `evidence_pipeline.py:34-40,108`; `run_week11_initial_evaluation.py:160`; per-case diff | The "5→12" headline contradicts the paper's own definition. The display-level gain is +1. The result is a displacement measure. | Fix the baseline description, R@5 numbers/definition and RQ1 framing; disclose the test-informed adoption |
| 3 150/150 | By construction | **Both.** Valid cross-store result and near-invariant; no control arm | `grounded_answer.py`, `citation_verifier.py`, RQ2 "A" ≡ "D" | H2 untested; no improvement claim possible | One sentence: by construction, no unconstrained arm, H2 not tested |
| 4 E4 tamper testing | 111/111 | **Qualified.** 111 = 3×37 incl. extension; Base-30 = 90/90; function-level probes. Unit tests verified (no date-tamper test) | `run_rq2_37.py:144-161`; `rq2_case_results.csv`; test files | Shows the gate works; not an evaluation outcome | Optional: cite 90/90 probes on Base-30, labelled as positive controls |
| 5 RQ-label mismatch | Labels reused | **Confirmed.** Narrowing is intentional, labels misleading | §III-A vs spec | Implies canonical RQs were answered | One clause linking them to the canonical RQs; reframe RQ1 |
| 6 Temporal rule | Deviation unnamed | **Confirmed**, but the paper documents its own rule fully; deviation recorded in the freeze | `temporal.py`; `datasets.json`; freeze `known_limitation` | Stricter rule (recall cost already stated) | Should-fix: note it is stricter than a date-level rule; fix the "temporal existence" definition |
| 7 Generation | Not implemented | **Confirmed.** Never built; recorded as "IMPLEMENTED (stricter)" rather than a deviation | Code search; `model-feasibility.json`; scope audit | §III-A implies an unevaluated component exists | Say the output layer is extract-only and no generation was built |
| 8 Answer-key chronology | (not raised) | Statement true for reported scoring; earlier dev spot checks existed | Manifest; round freeze 2026-08-30; finalized 2026-09-01 | No validity issue | Optional: tighten the wording |
| 9 Leakage audit | (not raised) | **Reproduced.** Facts SHA match; salient 1/30; facts 14–19/30 by definition | Independent recomputation | Normal citation, not contamination; recovery concentrated in mentioning cases (12/19 vs 3/11) | Should-fix: one sentence of interpretation |
| 10 E1/E2 asymmetry | (not raised) | **Confirmed.** 6,003 vs 5,020 labelled docs | E1/E2 result artifacts | E1 > E2 comparison favours E1 | Should-fix: disclose |
| 11 81-test claim | 81 counted, unverified | **Claim false as stated.** 75 passed (recorded and re-run); 6 never executed | Audits, logs, rerun | Overstated verification | Replace with 75/81 wording |
| 12 Related work | Universal negative | **Partly confirmed.** Overbroad; AILA / IL-TUR omitted (verify) | Web search | Literature gap; reviewer risk | Scope the claim; consider adding verified Indian retrieval work |
| 13 Citation support | (not raised) | [6] partial; [3] core facts corroborated, specific counts and phrasing unverified | Abstract; secondary sources | Possible over-attribution | Soften the [6] claim; verify [3] details against the judgment |
| 14 2026 references | Verify | [11], [13], [14] verified; [15] bibliographic data verified by repo audit, "TaxFlow"/validity description unverified | Searches; `final_reference_resolution.md` | Citation-accuracy risk for [15] | Verify the [15] description or remove it |
| 15 Anonymity | Risk | No venue recorded; identity is fully exposed | Repo audit; tex | None if single-blind | Flag only; anonymise if double-blind |

## O. Decision

**1. Non-negotiable corrections** (otherwise the paper is inaccurate)
- Freeze-audit sentence (A).
- Recall@5 inconsistency. Either report the baseline as 11/30 under Table I's definition (selected), or redefine R@5 as raw rank ≤5 and state it applies to the mixed list. Abstract, contributions, §VIII-C, Table III and the Conclusion all depend on this (B).
- The baseline is a post-ranking filter, not "unfiltered BM25 … no temporal eligibility predicate" (B).
- Development chronology: the pre-ranking configuration was adopted after the 30-case test comparison, and the 7/9 dev result came afterwards (§VIII-E) (B).
- "Passes 81 tests" → 75 of 81 executed and passed (K).

**2. Interpretation changes**
- Present RQ1 as a characterisation of displacement whose direction is guaranteed by construction (B, E).
- 150/150 holds largely by construction; H2 was not tested; there was no unconstrained arm (C).
- Generation was not built (G).
- Link the paper's RQs to the canonical RQs (E).
- E1/E2 training-data asymmetry (J).
- Recovery is concentrated in cases whose facts discuss the authority (I).

**3. Optional clarifications**
- Base-30 positive-control probes, 90/90 (D).
- Temporal rule is stricter than the date-level rule; "temporal existence" definition (F).
- Answer-key wording (H).
- Soften the [6] claim; verify [3] and [15]; scope the Related Work negative and check AILA/IL-TUR (L).
- Anonymisation if the venue is double-blind (M).

**4. Do not change** (verified correct)
- E1/E2 1,503-case metrics.
- Majority baseline.
- McNemar p = 0.258 (238/213).
- 684/368/238/213 and the 30-case 18/3/3/6.
- 21→20 with the named cases.
- R@100 12→15 and final R@5 = 12/30.
- Authority P/R/F1 0.08/0.40/0.133 and the 0.20 ceiling.
- 12/3/15 buckets with ranks 15/28/78.
- 138/150 State 4.
- Era split 5/13/9/2/1.
- Corpus and alignment counts.
- Two-population separation.
- The fair 30-case E2 comparison.
- The bundled-intervention caveat.
- The list of unit-test rejection behaviours.
- The salient-term leakage figure (1/30).

**5. Paper status: CONDITIONAL GO.**
The final measured results (12/30, 15/30, 150/150, outcome metrics) are reproducible and correctly computed. Every non-negotiable item can be fixed with wording backed by existing artifacts, and no experiment needs to be rerun. The status becomes **NO-GO** if the corrections are not made. In particular, a headline "5/30→12/30" improvement that contradicts the paper's own Recall@5 definition, together with a development narrative that hides the test-informed configuration choice, would be a substantive research-validity misstatement.
