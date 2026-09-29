# Paper claim audit (Parts A–K, N–O evidence base)

Authoritative manuscript: `paper_master.tex` (55,994 bytes, SHA-256 9DE053A7C74F8807D86100C5D2FB9C93DDB602EFC140EE59B; modified 2026-09-22 18:08:51 UTC).
Built PDF: `paper_master.pdf` (293,984 bytes, SHA-256 3B35C27966D72EE7DABECBA6329A771E71ADBBBCA03E3DCAF; 10 pages, ~7,077 words).
Note: the paper was described to the auditor as "6–7 pages"; the built PDF is 10 pages (content + references).
Source: single `.tex` with inline `thebibliography` (15 entries); no `.bib` file. Figures: `figures/fig1_fig5` PDFs.
Older draft `Indian_Legal_XAI.docx` (27,166 bytes, 2026-09-06) is not authoritative.
Sections present: Title, Abstract, Keywords, Introduction, Related Work, Problem Formulation (+RQs), Corpus Construction and Auditing, System Design, Method, Citation and Provenance Protocol, Results, Error Analysis, Limitations and Threats to Validity, Responsible Use and Governance, Conclusion and Future Work, Reproducibility, Acknowledgment, References. No appendix.

## Part C — population audit
- 1517 pre-filter / 14 excluded / 1503 evaluated: terminology correct everywhere checked ("1,503 eligible", "After a shared sufficiency rule excluded 14 test records, the held-out prediction population contains 1,503"). Excluded IDs in `e1_baseline_results.json` match the audit's p6 eligibility log exactly. Status: PASS.
- 33 vs 30: answer key holds 33 entries (30 `evaluation` + 3 examples). The paper consistently says "30-case" for evaluation; no occurrence of an ambiguous "33" was found. Status: PASS.
- 30 vs 37: paper always stratifies (Base-30 / Extension-7 / Combined-37) and states the combined set is "a later expanded analysis, not the original frozen base". Status: PASS.
- ISSUE C1: Error Analysis (lines 854–857) says four cases "retrieved and selected the expected authority" including `1985_40`, but frozen flags show `1985_40` retrieved-at-100=True, selected=False (rank 78, listed under "Retrieved, not selected"). Required correction: "three retrieved and selected (2008_1629, 1981_187, 1982_29) plus 1985_40 retrieved but unselected, yet prediction still wrong."

## Part D — metric definitions
| metric | paper definition | implemented definition | match |
| Accuracy | implied standard share correct | sklearn accuracy_score, case-level | MATCH |
| Macro-F1 / class F1 | standard; Table II values | sklearn f1 average=macro / pos_label | MATCH |
| Recall@100 | authority anywhere in top-100 (Tab I) | evaluate_against_answer_key expected_authorities_retrieved, case share, denom 30 | MATCH |
| Recall@5 | authority among five selected/displayed (Tab I) | selected_measure matched_expected_authorities, case share, denom 30 | MATCH |
| Provenance validity | 7 fields + run membership (Tab I) | corpus field equality + run membership + duplicate/temporal checks | MATCH |
| Groundedness | verbatim + linked (Tab I) | assert_answer_grounded | MATCH |
| Authority consistency | source ID / norm citation / norm title+date (Tab I) | same three-way match | MATCH |
Rounding: 0.601464→0.6015, 0.593682→0.5937, 0.666667→0.6667, 0.603175→0.6032, 0.501663→0.5017, 0.334072→0.3341 — all consistent 4dp. No micro/macro confusion found.

## Part E — experiment wording
- E1: paper says C compared on validation, refit once on train+val, test once. Replay refit+evaluated deterministically (canonical IDENTICAL); the C-search itself was consumed, not re-run. Description accurate; "reconstructed E1" (line 825) is fair. CPU env. No overstatement found.
- E2: paper describes fine-tune config + pooling/selection rules. Replay was inference-only from checkpoint-6318 (training not re-run). Paper does not claim retraining in evaluation; wording accurate. GPU RTX 3050, fp16; inference deterministic across our two repeats (bit-identical records).
- E3/E4: recomputed end-to-end from source inputs (retrieval + selection + rendering + verification + shared-predictor inference). Strict byte hash differs only in fp16 mean-logit tails (max 7.7e-4); all labels, evidence IDs, flags, metrics identical. Paper must NOT be read as claiming byte-identical E3/E4 payloads; "identical confusion matrices" (true) and substantive-output equivalence are the supported phrasings.
- BM25: paper says only "a SQLite FTS5 BM25 index" and "index were rebuilt from the accepted corpus" — no byte-identity claim. Supported: same corpus/IDs/params + 30/30 ranking agreement on evaluated queries. Scope must stay at the evaluated query set.

## Part G — leakage scope (exact)
- Checked: top-5 selected sources vs dedup exclusions + canonical query ID (0/30 self), temporal violations in top-5 (0), 16/30 queries carry dedup exclusions, authority-recall metric unaffected by self-match by construction.
- NOT checked: top-100 candidate-level self-match; train/test and validation/test overlap beyond ILDC's fixed disjoint splits (consumed as given); extension-7 leakage (same gates per FREEZE_REPORT, not re-audited here).
- Forbidden generalization: do not convert "0/30 self in top-5" into "no data leakage whatsoever."

## Part H — answer-key corrections
- Paper: "20 passed, nine resolved sources failed direct content alignment, and one source was unresolved. One case was relinked ... nine flagged records were replaced ... 30/30 direct-content passes." Consistent with `answer_key_alignment_audit_corrected` (30 rows, summary pass 30) per subaudit; 2013_35 handled as query-source replacement (paper does not claim an authority change — verified no such sentence). The 1503/1517 filter discussion matches the 14-ID exclusion list. Status: PASS (artifact-based; mapping re-derivation not re-run).

## Part J — overclaim scan (selected)
- "never stand in for" / "never alters" / "never pooled" (design intents): SUPPORTED as architecture statements (separate code paths), not empirical guarantees.
- "guarantee that no displayed authority can post-date the matter" (line 218): PARTIALLY SUPPORTED — holds conditional on metadata correctness + fail-closed checks (0 violations observed on 30+7); word "guarantee" is strong; prefer "ensures under the stated metadata and fail-closed assumptions."
- "reproducible combination" (line 189): PARTIALLY SUPPORTED — E1/E2 exact, E3/E4 functional with fp16 caveat, freeze drift documented.
- "independently useful" audit (line 373): SUPPORTED as author assessment; factual counts verified.
- No "state-of-the-art", "superior", "significantly improves", "proves", "eliminates", "fully reproducible", "novel/first" claims found (paper explicitly disclaims first/novel at lines 187–188). "No production deployment claimed" explicit.
- Small-cohort generalization: paper contains explicit anti-generalization language (limits, strata, "descriptive", "exploratory"); no unsupported whole-domain generalization found.

## Part K — limitations coverage
Present: language/court scope, OCR noise + 3 exclusions, 30→37 size/era imbalance (43.3% 1980s), single authority, 17/37 residual gap, year granularity, bundled verification, non-independent/LLM review with duplicate-vector caution, prototype scale.
Missing / thin: (1) 14-case facts filter is described in corpus/method but not reframed as a limitation (acceptable; not a validity threat); (2) GPU fp16 logit non-determinism is documented in week16 but not named in the paper's limitations — ADD one sentence; (3) BM25 equivalence is behavioral (paper makes no byte claim, so nothing to correct, but a clarifying "ranking-level" phrase would pre-empt misreading); (4) TypeScript-compile evidence for the demo is claimed without a cited log.

## Part N — abstract/conclusion consistency
Every abstract/conclusion number traces to body tables: 37/30+7, 5391→11, 5/30→12/30, 12/30→15/30, 12/37 & 20/37, 185 citations, 17 absent, 1503, 56/56 (as presentation-only). "56/56" appears with the presentation-only qualifier in both places. No number appears that the body lacks. Terminology consistent (strata kept). Missing from abstract: fp16 caveat (minor; belongs in reproducibility section, which is present in body).
