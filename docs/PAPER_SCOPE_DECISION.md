# Paper-Level Scope Decision — NyayaTrace

Recorded 2026-10-09. This record sits beside the canonical project specification and does not modify it.

| Document | Role |
|---|---|
| [`docs/INDIAN_LEGAL_XAI.docx`](INDIAN_LEGAL_XAI.docx) | **Fixed Project Scope — Controlled Copy** of the canonical specification, *Explainable AI for Indian Legal Research: An Evidence-Grounded Framework — Canonical Project Specification, Document 3 (Final)*. It defines the overall Indian__legal_XAI scope. |
| This file | The paper-level scope decision for `submission/research_paper.tex`. It narrows what the manuscript studies; it does not narrow the project. |

## Decision

The overall scope of Indian__legal_XAI remains unchanged. The manuscript is an intentionally narrower research study within the broader legal research system.

The paper focuses on temporally constrained, provenance-verified evidence retrieval, including the retrieval consequences of applying temporal eligibility filtering before versus after BM25 ranking. Its findings are limited to the frozen evaluation configuration, corpus, implementation, and experiments reported in the manuscript. The paper is not intended to provide a comprehensive evaluation of every component or research question in the overall project.

The paper's exploratory RQ1 remains exploratory. The manuscript does not claim to have established H2/RQ2 or evaluated RQ3. It remains an extract-only study without generated legal answers.

The distinction between the canonical specification's date-level temporal rule, `decision_date <= case_date`, and the paper's year-level implementation, `decision_year < query_year`, remains an explicit limitation.

This decision records the selection of a paper-level research focus by the primary selector. It does not revise, replace, or reduce the overall project scope.

## How the manuscript reflects the decision

Checked against `submission/research_paper.tex` on 2026-10-09; `validate_final.py` asserts the quoted wording.

| Point | Manuscript wording (section) |
|---|---|
| Narrower than the project | "This paper asks two questions. Both are narrower than, and not identical to, the research questions of the broader project." (III-A) |
| RQ1 exploratory | "Base-30 informed configuration choices (Section VIII-D), so the RQ1 analysis is exploratory." (III-A); "it is not a causal test of retrieval quality" (VIII-B) |
| H2 not tested | "No unconstrained generation or evidence-selection arm was evaluated, so the broader H2 comparison was not tested." (X) |
| RQ3 not evaluated | "human-rated explanation quality (RQ3) was not evaluated" (X); "RQ3 is deferred" (III-A) |
| Extract-only | "no generation component was built or evaluated" (III-A, X) |
| Temporal rule | "uses a stricter year-level rule rather than a date-level one … Same-year sources are treated as ambiguous and excluded" (III) |

The paper's two questions are paper-level questions. They are not additions to the specification's three research questions ("Only the following three research questions are in scope").

## Change-control review: the 1,979-position retrieved-set finding

**Specification rule** (Evaluation Metrics, "Note on scope", verbatim): "Temporal Violation Rate is the sole required temporal integrity metric. Named sub-decompositions (e.g., separately reporting retrieved-set exposure versus final-citation exposure, or a prediction delta across E3/E4) were reviewed and are explicitly **not** adopted as additional required metrics, since they are not part of the approved baseline. Nothing prevents the implementation team from computing such breakdowns internally for debugging, but they must not be reported as frozen evaluation deliverables or used to imply a broader evaluation objective than the one specified here."

**Repository record.** `config/week11_evaluation_round.json` records the superseded post-ranking control's candidate status counts: `{"eligible": 764, "later_year_ineligible": 1712, "same_year_ambiguous": 267}`, so 1,979 of 2,743. It also records the reporting decision: "Two temporal exposure-rate metrics were removed on the project mentor's guidance; direct status counts remain."

**Manuscript presentation.**
- Section VIII-B, in prose only: "In the control, later-year and same-year judgments filled 1,979 of the 2,743 non-duplicate top-100 candidates."
- It is a direct count from the superseded post-ranking control, not a rate.
- It is not in any metric table; Tables II–IV do not list it.
- The integrity measure reported for the final system is temporal violations, 0 of 150 (Table IV), consistent with Temporal Violation Rate.
- RQ1 asks "how much retrieval capacity do later and same-year judgments occupy".

**Determination.**
- The count is not reported as a frozen evaluation deliverable or as an exposure-rate metric.
- Its form, a direct status count, matches the documented mentor guidance.
- The paper states that its questions are narrower than the project's, so it does not imply a broader evaluation objective for the project.
- One point is a matter of judgment, not a rule breach: RQ1 makes the occupancy the subject of a paper-level question. This record documents that choice.
- The finding is retained unchanged and has not been relabelled.

**Approval status.**
- The specification requires that permitted changes "be documented in the reproducibility record". It does not explicitly require separate supervisor or mentor approval for a paper-level focus.
- No supervisor or mentor approval of this paper-level focus is documented in the repository, and none is claimed here.
- If the authors' institution requires such approval, it remains **pending** until recorded.

**Why this is a separate file.** The machine-readable reproducibility record, `config/reproducibility_freeze.json`, is generated by `scripts/build_reproducibility_freeze.py` and holds the frozen hash manifest that `validate_final.py` audits. This decision changes no frozen setting, configuration, metric or result, so the record was not edited.

## Controlled copy: conversion record

| Item | Value |
|---|---|
| Source | `Indian_Legal_XAI.pdf` (repository root, untracked; 20 pages, US Letter; exported from Microsoft Word 2016) |
| Source SHA-256 | `5124f5cf06362442c50c922d37ac15d360e30a50839e06aea119948d4f8bd0b1` |
| Controlled copy | `docs/INDIAN_LEGAL_XAI.docx` |
| Controlled copy SHA-256 | `f8a210b0e129d8c3154c3ab8631a337ef629924d205f9dca1f992d0e4516767e` |
| Conversion date | 2026-10-09 |

**Method.** Text, inline bold, italic and monospace, headings, bullet lists, line diagrams and all ten tables, plus the boxed "Document status and governing rule" table, were taken from the source PDF's own layout. Nothing was summarised, paraphrased or corrected. Microsoft Word 16 opened the file, regenerated the table of contents and saved it.

**Verification (all performed 2026-10-09).**
1. **Word sequence:** the DOCX body matches `experiments/audit_fixes/spec_full_text.txt`, the text of the original Word source, exactly. That is 4,081 of 4,081 words in the same order, with zero differences.
2. **Word multiset against the PDF's own text extraction:** the only differences are explainable.
   - 95 `•` glyphs, which are now Word list bullets.
   - Header rows that the PDF repeats on continuation pages; the DOCX marks them as repeating header rows instead.
   - One reading-order artifact of the PDF text layer in the E2 table row.
3. **Diagrams:** the three line diagrams (output contract, system architecture, citation protocol) are identical line for line.
4. **Table of contents:** 34 entries, with titles identical to the source TOC in the same order.
5. **Opens in Word:** 20 pages, 12 tables, 34 headings. The exported PDF of the DOCX contains every source word.
6. **Visual inspection:** the rendered pages were inspected.

**Intentional, non-substantive differences.**
- A document-control page, a running header ("INDIAN_LEGAL_XAI — Fixed Project Scope — Controlled Copy") and page numbers were added.
- Table-of-contents page numbers reflect the DOCX pagination.
- Table rows are kept on one page instead of splitting across pages.
- The author and last-modified-by metadata fields are set to "Yuvraj Singh".

After verification, the source PDF was removed from the working tree. It was never committed, and its SHA-256 above identifies it.
