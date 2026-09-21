# Independent Audit Report: NyayaTrace IEEE Conference Submission Package

**Date of Audit:** September 21, 2026  
**Audited Directory:** `submission/final/`  
**Governing Documents & Baseline:**
- Scope Document: *Canonical Project Specification, Document 3 (Final)* (`Indian_Legal_XAI.docx`)
- IEEE Conference Template / `IEEEtran.cls` (v1.8b)
- Reproducibility Baseline: `config/reproducibility_freeze.json`

---

## 1. Executive Verdict

### **VERDICT: SUBMIT AFTER FIXES**

The core scientific research, experimental arithmetic, data integrity, and reproducibility foundations of NyayaTrace are exceptionally sound. There are **zero fabricated numbers**, **zero unexplained mathematical discrepancies**, **zero Type 3 fonts**, and **zero compilation errors** in the LaTeX build. All 15 cited references are confirmed real, verifiable peer-reviewed papers or official Supreme Court judgments.

However, the package cannot be submitted in its current state due to **three MAJOR formatting and packaging integrity defects** that will cause immediate rejection or desk disqualification by an IEEE conference editorial chair:
1. **Citation Order Violation (IEEE Conference Style):** Citations in the body text appear out of numerical order (e.g., `[13]`, `[14]`, `[6]`, `[1]`, `[2]`, `[12]`) because `\begin{thebibliography}` lists items in an arbitrary sequence rather than in order of first appearance in the text.
2. **Manifest and Package Hash Drift:** `submission/final/MANIFEST.md` contains duplicate and conflicting SHA-256 records for `paper_master.pdf`, `paper_master.tex`, and `nyayatrace_submission_package.zip`. Neither hash listed for `paper_master.pdf` matches the actual PDF on disk or inside the zip.
3. **Epistemological Framing Tension:** Line 650 and Table III designate the post-freeze 37-case expansion as the "principal evaluation," which directly conflicts with Section IV (line 409), Addendum RR-03, and the canonical specification requiring the frozen 30-case benchmark to remain the primary evaluation standard.

---

## 2. Summary of Findings by Severity

| Severity | Count | Summary of Items |
|---|:---:|---|
| **BLOCKER** | **0** | No critical blockers that invalidate scientific claims or crash the toolchain. |
| **MAJOR** | **3** | (1) References cited out of numerical order in text; (2) Manifest hash conflicts & zip desynchronization; (3) Combined-37 framed as "principal" evaluation vs frozen Base-30 baseline requirement. |
| **MINOR** | **3** | (1) Abstract length is 254 words (exceeds IEEE 250-word ceiling); (2) Causal overclaim in Intro line 135-136 contradicts Section X limitation line 947-948; (3) Page 10 Column 2 is completely blank (unbalanced final columns). |
| **NIT** | **1** | (1) Abbreviations (`AI`, `ILDC`, `LLM`) used in abstract without inline expansion. |

---

## 3. Phase-by-Phase Findings with Concrete Evidence

### Phase 1: Build and Format Audit

- **Compilation Status (`PASS`):**
  - Toolchain: pdfTeX 3.141592653-2.6-1.40.26 (TeX Live 2025/dev/Debian) via Docker container `nyayatrace-texlive:latest`.
  - Command: `pdflatex -interaction=nonstopmode paper_master.tex` (x3).
  - Output: `0 errors (!)` , `0 Overfull \hbox`, `0 undefined references/citations`.
- **Page Count & Geometry (`PASS`):**
  - Tool: `pdfinfo paper_master.pdf`.
  - Pages: Exactly 10 pages (`Pages: 10`).
  - Page Size: Exactly US Letter (`Page size: 612 x 792 pts (letter)`).
- **Font Compliance (`PASS`):**
  - Tool: `pdffonts paper_master.pdf`.
  - Fonts: 22 fonts total, 22/22 embedded (`emb: yes`), 0 Type 3 fonts (`Type 1`: 17, `CID TrueType`: 5). Fully compliant with IEEE PDF eXpress guidelines.
- **Document Structure (`PASS`):**
  - `paper_master.tex:1`: `\documentclass[conference]{IEEEtran}` (standard IEEE conference class).
  - `paper_master.tex:77`: `\begin{IEEEkeywords}...\end{IEEEkeywords}` present.
  - `paper_master.tex:1056`: `\section*{Acknowledgment}` uses standard IEEE single-author spelling.
- **Visual Page Layout & Figures (`PASS`):**
  - Visual inspection of rendered PNG pages (`scratch/pages/page-01.png` through `page-10.png`):
    - Page 1: 2x2 author grid neatly aligned; abstract and keywords properly formatted.
    - Page 2: Fig. 1 (Outcome prediction latency/memory trade-off) clear, legible labels.
    - Page 4: Fig. 2 (Case coverage funnel) clear; labels `12`, `8`, `17` fully visible; legend upper-left unobstructed.
    - Page 5: Fig. 3 (Integrity vs verification) clean vector lines.
    - Page 6: Fig. 4 (Pathway investigation) x-axis tick labels rotated 25°, no collision; legend in upper headroom clear; left y-axis spine cleanly bounded `[0, 1]`.
    - Page 8: Fig. 5 (Explanation dimension comparisons) horizontal bars legible.
- **Abstract Length (`FAIL - MINOR`):**
  - *Evidence:* `paper_master.tex:51-74`.
  - Word count: Exactly 254 words. IEEE Conference author instructions specify: *"The abstract must be between 150–250 words."* (Over by 4 words).
- **Column Balance on Final Page (`FAIL - MINOR`):**
  - *Evidence:* `scratch/pages/page-10.png`.
  - Page 10 Column 1 contains references `[6]` through `[15]`. Page 10 Column 2 is 100% blank. IEEE transactions and conference style mandates balancing columns on the final page (`\IEEEtriggeratref` or `flushend`).
- **Citation Sequencing (`FAIL - MAJOR`):**
  - *Evidence:* `scratch/check_citations.js` execution output; `paper_master.tex:89,91,97`.
  - Body text cites references in order: `\cite{dahl2024}` (`[13]`), `\cite{nay2023}` (`[14]`), `\cite{poojasingh2026}` (`[6]`), `\cite{malik2021}` (`[1]`), `\cite{paul2023}` (`[2]`).
  - IEEE Section IV.B formatting rules require references to be numbered in order of first appearance (`[1]`, `[2]`, `[3]`).

---

### Phase 2: Internal Consistency Checklist

All mathematical relationships, set-theoretic partitions, and cross-references within `submission/final/paper_master.tex` were audited. Every identity holds exactly:

| Mathematical Relationship / Claim | Paper Text Location | Formula / Check | Audit Status | Evidence / Derivation |
|---|---|---|:---:|---|
| Raw tax judgments filter | Lines 127–128, 360–365 | $5{,}391 - 11 = 5{,}380$ | **PASS** | 5,391 raw candidates; 11 content-aligned; 5,380 discarded. |
| Passage index composition | Lines 369–370 | $1{,}304 + 7{,}623 = 8{,}927$ | **PASS** | 1,304 primary + 7,623 secondary passages = 8,927 total passages. |
| Base-30 taxonomy breakdown | Lines 395–397 | $5+13+9+2+1 = 30$ | **PASS** | Direct (5), Interpretation (13), Procedural (9), Constitutional (2), Retrospective (1); $13/30 = 43.33\%$. |
| Total query counts | Lines 110–111, Table IV | $30 \times 5 = 150$; $7 \times 5 = 35$; $150+35 = 185$ | **PASS** | 5 citations per case across 30 base cases (150) and 7 extension cases (35), totaling 185 queries. |
| Table III Recall & Recovery | Table III, Lines 660–675 | Base-30: $12/30 = 0.40$, $15/30 = 0.50$; Extension-7: $0/7 = 0.0$, $5/7 = 0.7143$; Combined-37: $12/37 = 0.324324$, $20/37 = 0.540541$ | **PASS** | Exact match with `experiments/rq1/rq1_results.json`. Fig. 2 funnel matches: $12 + 8 + 17 = 37$; $12 + 3 = 15$; $15 + 2 = 17$ absent. |
| Authority Precision & Ceiling | Table IV, Lines 693–713 | $12/150 = 0.08$; Structural ceiling $30/150 = 0.20$; $0.08 / 0.20 = 40.0\%$; F1 = $0.1333$ | **PASS** | Exactly 1 expected authority per query among 5 displayed; 138 non-matching valid citations. |
| Combined-37 Outcome Prediction | Table III, Lines 670–685 | Acc: $24/37 = 0.648649$; Base (20) + Ext (4) = 24 | **PASS** | Confusion matrix `[[6, 3], [10, 18]]`; Diagonal: $6 + 18 = 24$; Macro-F1: $0.607347$. |
| Table V Error Overlap Totals | Table V, Lines 834–848 | Full test: $684 + 238 + 213 + 368 = 1{,}503$; Base-30: $18 + 3 + 3 + 6 = 30$ | **PASS** | Matches `artifacts/week12_prediction_cross_reference.json` exactly to the unit. |
| Table VI Case Partitioning | Table VI, Lines 869–895 | $12 + 3 + 15 = 30$; State (4) absent: $18$ of $30$ | **PASS** | 12 selected + 3 unselected + 15 absent = 30; $30 - 12 = 18$ absent from top-5. |
| Freeze Hash Totals | Lines 1038–1040 | $28 \text{ (byte-exact)} + 1 \text{ (CRLF)} + 10 \text{ (metadata)} = 39$ | **PASS** | Exact partition of the 39 unique paths in `config/reproducibility_freeze.json`. |
| Float & Section References | Throughout `.tex` | 19 `\ref{}` calls | **PASS** | All 19 resolved to valid `\label{}` tags (`scratch/check_refs.js`). |

---

### Phase 3: Claims vs. Artifacts Traceability Table

Every empirical claim and table in `submission/final/paper_master.tex` was traced to source JSON artifacts in `artifacts/`, `experiments/`, and `answer_key/`:

| Paper Claim / Table | Reported Value in Paper | Ground-Truth Artifact Key & File | Match Status | Verification Evidence |
|---|---|---|:---:|---|
| **Corpus Document Count** | 39,069 raw PDFs, 39,066 documents, 2,036,981 chunks | `artifacts/corpus_readiness.json`: `expected_pdfs: 39069`, `documents_with_chunks: 39066`; `artifacts/bm25_index.json`: `chunks_indexed: 2036981` | **PASS** | Exact match across all corpus build logs. |
| **Corpus Record Identity** | 2,343,435 raw JSONL records | `artifacts/ecourts_corpus_identity.json`: `jsonl_record_count: 2343435` | **PASS** | Exact match. |
| **Table II: Majority Class** | Acc: 0.5017, Macro-F1: 0.3341 ($n=1,503$) | `artifacts/e1_e2_comparison.json`: `majority_class_baseline.accuracy: 0.501663`, `macro_f1: 0.334072` | **PASS** | Traced and correctly rounded. |
| **Table II: E1 TF-IDF+LR** | Acc: 0.61344, Macro-F1: 0.612342 ($n=1,503$) | `artifacts/e1_baseline_results.json`: `validation_candidates[C=10]`, `accuracy: 0.61344`, `macro_f1: 0.612342` | **PASS** | Exact match to 6 decimal places. |
| **Table II: E2 Mean Logits** | Acc: 0.596806, Macro-F1: 0.592358 ($n=1,503$) | `artifacts/e2_chunk_pool_results.json`: `test_document_metrics.mean_logits.accuracy: 0.596806`, `macro_f1: 0.592358` | **PASS** | Exact match to 6 decimal places. |
| **Table II: E2 Majority Vote** | Acc: 0.6015, Macro-F1: 0.5937 ($n=1,503$) | `artifacts/e2_chunk_pool_results.json`: `test_document_metrics.majority_vote.accuracy: 0.601464`, `macro_f1: 0.593682` | **PASS** | Traced and correctly rounded. |
| **Table II: E3 Evidence-Augmented** | Acc: 0.666667, Macro-F1: 0.603175 ($n=30$) | `artifacts/e3_e4_evidence_augmented_evaluation.json`: `test_document_metrics.accuracy: 0.666667`, `macro_f1: 0.603175` | **PASS** | Exact match. |
| **Table III: Base-30 Retrieval** | R@5: 0.40, R@100: 0.50 | `experiments/rq1/rq1_results.json`: `strata.base30.e3_retrieval.recall_at_5: 0.4`, `recall_at_100: 0.5` | **PASS** | Exact match. |
| **Table III: Extension-7** | R@5: 0.00, R@100: 0.7143, Acc: 0.5714, F1: 0.5714 | `experiments/rq1/rq1_results.json`: `strata.extension7.e3_retrieval.recall_at_100: 0.714286`, `accuracy: 0.571429` | **PASS** | Exact match. |
| **Table III: Combined-37** | R@5: 0.324324, R@100: 0.540541, Acc: 0.648649, F1: 0.607347 | `experiments/rq1/rq1_results.json`: `strata.combined37.e3_retrieval.recall_at_5: 0.324324`, `recall_at_100: 0.540541`, `accuracy: 0.648649`, `macro_f1: 0.607347` | **PASS** | Exact match to 6 decimal places. |
| **Table IV: Integrity Base-30** | Grounding: 1.00 (150/150), Provenance: 1.00 (150/150), Temp Violations: 0 | `artifacts/week11_temporal_prerank_evaluation.json` & `experiments/rq1/rq1_results.json`: `grounding_passed: 150`, `temporal_violations: 0` | **PASS** | Fail-closed verifier passes 150/150. |
| **Candidate Logs** | 3,000/3,000 eligible candidates logged | `artifacts/week11_temporal_preranking_investigation.md`: *"The final candidate log contains 3,000/3,000 eligible candidates"* ($30 \times 100$) | **PASS** | Verified in artifact. |
| **Table V: Error Overlap** | Full: 684 / 238 / 213 / 368; Base-30: 18 / 3 / 3 / 6 | `artifacts/week12_prediction_cross_reference.json`: `full_test_n1503_E1_E2_outcome_disagreement` & `answer_key_cohort_n30.E1_E2_outcome_disagreement` | **PASS** | Exact counts verified. |
| **Table VI: Partition Cases** | 12 selected, 3 unselected, 15 absent | `artifacts/week11_error_analysis.json`: `correct_authority_retrieved_and_selected` (12), `retrieved_not_selected` (3), `absent` (15) | **PASS** | All 30 individual case strings match verbatim. |
| **RQ3: LLM Raters** | 14 cases, 4 evaluators, 112 ratings, 56/56 preferences | `experiments/rq3/rq3_results.json`: `n_cases: 14`, `n_evaluators: 4`, `n_display_ratings: 112`, `preference_counts...structured: 56` | **PASS** | Unanimous preference, identical DeepSeek and Luna vectors disclosed. |
| **Random Seeds & Checkpoints** | E1: 202605, E2: 202607, InLegalBERT `b5ecfed8...`, ckpt-6318 `924a5bb9...` | `config/reproducibility_freeze.json` & `artifacts/e2_chunk_pool_results.json` | **PASS** | Hash matches committed checkpoint weights. |

---

### Phase 4: Claim Strength and Causal Language Analysis

A line-by-line semantic scan of `paper_master.tex` reveals exemplary restraint in general, but highlights one notable internal causal tension:

- **Section X Limitations Disclosures (`EXEMPLARY PASS`):**
  - Line 810: *"participated, no significance test was run, and nothing about human preference or legal correctness follows."*
  - Line 937: *"does not establish a causal attribution for the remaining gap."*
  - Line 948: *"The pre-ranking temporal filter, query formulation, and self-match guard were developed in sequence and cannot isolate any single component's causal contribution."*
  - Line 1000: *"does not guarantee that the system found the expected authority."*
- **Causal Attribution Inconsistency (`FAIL - MINOR`):**
  - *Evidence:* Line 135–136 states:
    > *"Pre-ranking temporal eligibility... On the held-out evidence set this change moved Recall@5 from 5/30 to 12/30 without regressing any prior success."*
  - *Conflict:* Line 135–136 attributes the entire gain from 5/30 to 12/30 strictly to the pre-ranking temporal eligibility bullet. However, the abstract (lines 62–64) attributes this gain jointly to *"pre-ranking temporal eligibility with salient-term queries and a self-match guard"*, and Section X (lines 947–948) explicitly cautions that the system *"cannot isolate any single component's causal contribution."*
  - *Verdict:* The phrasing in line 135–136 slightly overclaims single-component causality compared to the disciplined multi-component formulation in lines 62–64 and lines 947–948.

---

### Phase 5: Scope Compliance vs. Document 3 (`Indian_Legal_XAI.docx`)

Audited against *Canonical Project Specification, Document 3 (Final)* and `experiments/SCOPE_CONFORMANCE_AUDIT.md`:

| Scope Dimension | Document 3 Requirement | Paper Implementation | Status | Audit Findings & Evidence |
|---|---|---|:---:|---|
| **Decision-Support Identity** | Must assist human experts; NO autonomous AI judge | Line 55: non-inferential citations; Line 1053: non-autonomous | **PASS** | Fully compliant. |
| **Research Questions** | Exactly 3 RQs (RQ1 Grounding, RQ2 Provenance, RQ3 Structured Expl) | Line 245: *"There are exactly three research questions."* | **PASS** | Fully compliant; no spurious "RQ4" added. |
| **Model Families (E1–E4)** | E1 (TF-IDF), E2 (InLegalBERT), E3 (BM25), E4 (Verifier) | Lines 450–550 define E1–E4; frozen configs used | **PASS** | Exact correspondence with specification. |
| **Prohibited Techniques** | NO GraphRAG, multi-agent frameworks, dense semantic retrieval | Local FTS5 BM25 only; 0 GraphRAG/agent hits | **PASS** | Fully compliant; strict extract-only design. |
| **Language & Jurisdiction** | English core; Indian Supreme Court only | ILDC + eCourts Supreme Court judgments | **PASS** | English-only; no scope creep. |
| **Human Oversight Disclosure** | Human validation required for user-facing transparency | Lines 790–815 disclose 4 LLM raters as exploratory only | **PASS WITH LIMITATION** | Documented transparently; no human benefit claimed. |
| **Frozen Benchmark Primacy** | Primary evaluation must be on the frozen reference set | Table III Caption & Line 650 label Combined-37 as "principal" | **FAIL - MAJOR** | Combined-37 was constructed post-freeze (`answer_key/extension_v6/FREEZE_REPORT.md`). Elevating it over frozen Base-30 violates benchmark preregistration principles. |

---

### Phase 6: References Web Search Verification

All 15 bibliographic references were individually queried against live scholarly indices (ACL Anthology, ACM Digital Library, NeurIPS, IEEE Xplore, Oxford Academic, Indian Kanoon, Dr. Ambedkar International Centre/IBBI):

| Ref # | BibTeX Key | Authors | Title | Venue & Date | Page / Volume | Web Verification Status | In-Text Context & Findings |
|:---:|---|---|---|---|---|:---:|---|
| **[1]** | `malik2021` | V. Malik et al. | ILDC for CJPE: Indian Legal Documents Corpus... | ACL-IJCNLP 2021 | pp. 4046–4062 | **VERIFIED (100%)** | Supplies prediction benchmark & splits. Confirmed real. |
| **[2]** | `paul2023` | S. Paul et al. | Pre-trained Language Models for the Legal Domain... | ICAIL 2023 | pp. 187–196 | **VERIFIED (100%)** | Introduces InLegalBERT. Confirmed real. |
| **[3]** | `taxflow2026` | V. R. Karna et al. | A Hybrid RAG-LLaMA Framework for Scalable... | Appl. Artif. Intell., 2026 | Vol. 40, Art. 2626097 | **VERIFIED (100%)** | Introduces TaxFlow; shares statutory validity concerns. Confirmed real. |
| **[4]** | `casefacts2026` | A. R. Putta et al. | CaseFacts: A Benchmark for Legal Fact-Checking... | ACL 2026 | pp. 17246–17265 | **VERIFIED (100%)** | 6,294 claims, Supported/Refuted/Overruled. Confirmed real (arXiv:2601.17230). |
| **[5]** | `lextime2025` | C. Barale et al. | LexTime: A Benchmark for Temporal Ordering... | EMNLP 2025 Findings | pp. 5220–5236 | **VERIFIED (100%)** | 512 instances on temporal legal events. Confirmed real. |
| **[6]** | `poojasingh2026` | Supreme Court of India | Pooja Ramesh Singh v. J&K Bank Ltd. | 2026 INSC 668 (July 2, 2026) | Bench: Narasimha & Aradhe, JJ. | **VERIFIED (100%)** | Landmark ruling striking down NCLT orders based on fake AI cases. Confirmed real. |
| **[7]** | `robertson2009` | S. Robertson, H. Zaragoza | The Probabilistic Relevance Framework: BM25... | FnT in Inf. Retr., 2009 | Vol. 3, pp. 333–389 | **VERIFIED (100%)** | Canonical BM25 reference. Confirmed real. |
| **[8]** | `smith2007` | R. Smith | An Overview of the Tesseract OCR Engine | ICDAR 2007 | Vol. 2, pp. 629–633 | **VERIFIED (100%)** | Foundational Tesseract OCR reference. Confirmed real. |
| **[9]** | `coliee2023` | R. Goebel et al. | Summary of the Competition on Legal Information... | ICAIL 2023 | pp. 472–480 | **VERIFIED (100%)** | COLIEE 2023 competition summary. Confirmed real. |
| **[10]** | `legalbench2023` | N. Guha et al. | LegalBench: A Collaboratively Built Benchmark... | NeurIPS 2023 (D&B) | Vol. 36 | **VERIFIED (100%)** | 162 tasks measuring legal reasoning. Confirmed real. |
| **[11]** | `casehold2021` | L. Zheng et al. | When Does Pretraining Help?... CaseHOLD... | ICAIL 2021 | pp. 159–168 | **VERIFIED (100%)** | Carole Hafner Best Paper; 53k holdings. Confirmed real. |
| **[12]** | `shukla2022` | A. Shukla et al. | Legal Case Document Summarization... | AACL-IJCNLP 2022 | pp. 1048–1064 | **VERIFIED (100%)** | Legal summarization with practitioner ratings. Confirmed real. |
| **[13]** | `dahl2024` | M. Dahl et al. | Large Legal Fictions: Profiling Legal Hallucinations... | J. Legal Analysis, 2024 | Vol. 16, pp. 64–93 | **VERIFIED (100%)** | Legal hallucination rates (58%–88%). Confirmed real. |
| **[14]** | `nay2023` | J. J. Nay | Large Language Models as Fiduciaries... | arXiv:2301.10095, 2023 | Preprint | **VERIFIED (100%)** | Legal standards for communicating with AI. Confirmed real. |
| **[15]** | `lewis2020` | P. Lewis et al. | Retrieval-Augmented Generation for Knowledge... | NeurIPS 2020 | Vol. 33, pp. 9459–9474 | **VERIFIED (100%)** | Foundational RAG architecture paper. Confirmed real. |

---

### Phase 7: Package Integrity and Hash Consistency

Audit of `submission/final/MANIFEST.md` against on-disk files and `nyayatrace_submission_package.zip`:

- **Archive Integrity (`PASS`):**
  - Zip path: `submission/final/nyayatrace_submission_package.zip`.
  - Arcnames: All paths use clean, standard Unix forward-slashes (`figures/fig1_outcome.pdf`, etc.).
  - File composition: Contains `paper_master.pdf`, `paper_master.tex`, and all 5 vector figures.
- **Manifest Hash Corruption (`FAIL - MAJOR`):**
  - *Evidence:* Lines 33–38 of `submission/final/MANIFEST.md` read:
    ```markdown
    - `paper_master.pdf`: `d68dd159e03e7946ae5c14468c322dfb3044a49871bb241be04764c463dd6d73`
    - `paper_master.tex`: `2ba3d769a755ccf3ac26ff1cfcd526d7c8f54f5aea7f4343dabccbf0a50ec828`
    - `nyayatrace_submission_package.zip`: `1a92de4fc63b01f75a7f6c21e7c001703d2e9346c99edc20be4ce57319c4a420`
    - `paper_master.pdf`: `47854421433e25a2633a4f79fadc36701084ddf3601dc145d15c17ed978acfed`
    - `paper_master.tex`: `a8d63b045e2514dc3392f22abb8ef82ff4988201914ce27fc40b75c2067530fd`
    - `nyayatrace_submission_package.zip`: `054f471bbaed245cf2913690d0e4778064ef1fff40cd4d8bdb78b2ad02412863`
    ```
  - *Finding 1:* The manifest duplicates the entries for the PDF, TeX, and ZIP archives.
  - *Finding 2:* The actual on-disk hash of `paper_master.pdf` is `0ef0e88f1954da8e899650dbca5aec13b7431eb1bd7c969b1cb16cbe30451ef9` (due to the latest compilation). Neither manifest entry matches the on-disk file.
  - *Finding 3:* Inside `nyayatrace_submission_package.zip`, `paper_master.pdf` matches `47854421...`, which is out of date with the on-disk PDF.
- **Stale Workspace Deliverables (`PASS WITH WARNING`):**
  - Root directory `submission/` contains older artifacts (`submission/paper.pdf`, `submission/paper.md`, `submission/paper.html`, and `submission/MANIFEST.md`) dating from earlier milestones. The active, canonical package in `submission/final/` is isolated, but authors must ensure venue uploaders pull strictly from `submission/final/`.

---

## 4. Unverified / Not Checked Items

Every reference, table, and code claim was checked. No items were left unexamined:
- **References [1]–[15]:** 100% verified via web search and official digital libraries. None are unverified or fabricated.
- **Figures 1–5:** 100% verified visually and structurally.
- **Tables I–VI:** 100% verified against underlying JSON artifacts.
- **Automated Tests:** 81 unit tests in `tests/` confirmed present and passing.

---

## 5. Recommended Actions Ranked by Priority

To prepare `submission/final/` for flawless conference submission, execute the following fixes in order:

### Priority 1: Re-sequence `\begin{thebibliography}` (MAJOR)
Reorder the `\bibitem` entries in `submission/final/paper_master.tex` to match the exact order of first citation in the paper:
1. `dahl2024` (currently [13] -> become [1])
2. `nay2023` (currently [14] -> become [2])
3. `poojasingh2026` (currently [6] -> become [3])
4. `malik2021` (currently [1] -> become [4])
5. `paul2023` (currently [2] -> become [5])
6. `shukla2022` (currently [12] -> become [6])
7. `coliee2023` (currently [9] -> become [7])
8. `legalbench2023` (currently [10] -> become [8])
9. `casehold2021` (currently [11] -> become [9])
10. `taxflow2026` (currently [3] -> become [10])
11. `casefacts2026` (currently [4] -> become [11])
12. `lextime2025` (currently [5] -> become [12])
13. `lewis2020` (currently [15] -> become [13])
14. `robertson2009` (currently [7] -> become [14])
15. `smith2007` (currently [8] -> become [15])

### Priority 2: Synchronize Manifest and Package Zip (MAJOR)
1. Clean up duplicate hash lines in `submission/final/MANIFEST.md`.
2. Compile `paper_master.tex` using `pdflatex` (x3).
3. Re-package `submission/final/nyayatrace_submission_package.zip` with the newly compiled `paper_master.pdf`, `paper_master.tex`, and `figures/*.pdf`.
4. Compute final SHA-256 hashes for `paper_master.pdf`, `paper_master.tex`, and `nyayatrace_submission_package.zip`, and record them uniquely in `MANIFEST.md`.

### Priority 3: Reconcile Principal Benchmark Terminology (MAJOR)
In line 650 and Table III caption, soften "The principal RQ1 result uses the combined 37-case population" to clarify that the frozen 30-case set is the primary preregistered benchmark, while the 37-case set represents the additive, post-freeze expansion.

### Priority 4: Trim Abstract by 4 Words (MINOR)
Edit `paper_master.tex` lines 51–74 to reduce total word count from 254 words to $\le 250$ words to satisfy the strict IEEE ceiling.

### Priority 5: Balance Columns on Page 10 (MINOR)
Add `\IEEEtriggeratref{11}` (or use `\usepackage{balance}` / `\balance`) immediately before the bibliography so that references `[1]` through `[10]` appear in Column 1 and `[11]` through `[15]` appear in Column 2, eliminating the blank column on Page 10.

### Priority 6: Align Causal Phrasing in Line 135–136 (MINOR)
Harmonize line 135–136 with lines 62–64 and Section X (line 947–948) to state that the recall increase from 5/30 to 12/30 resulted from the combined pre-ranking temporal filter, query formulation, and self-match guard, avoiding single-component causal attribution.

