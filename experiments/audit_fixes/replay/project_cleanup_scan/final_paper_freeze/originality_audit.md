# Scholarly Originality and Source-Overlap Audit

**Date:** 2026-09-29

> **Note:** This document represents a genuine scholarly source-overlap and attribution audit. It is explicitly **NOT** an "AI-detector" evasion exercise, and no text was manipulated to lower probability scores from commercial detection tools.

> [!IMPORTANT]
> **Audit Scope Limitation:** No external database query was performed against Crossref, Google Scholar, Semantic Scholar, or commercial plagiarism services (e.g., Turnitin, iThenticate). The audit examined: the manuscript against its cited references, against this repository's own technical documentation, and against standard academic phrasing conventions. This limitation means the audit **cannot certify the absence of undetected overlap** in the broader scholarly literature. It is a targeted scholarly source-overlap review, not a full-coverage plagiarism scan.

## A. Audit Scope
The complete canonical manuscript (`paper_master_final.tex`) was analyzed for:
- Textual overlap against cited literature
- Attribution of source-derived material
- Standard academic phrasing versus original technical prose
- Internal consistency with the repository's own audit artifacts

## B. Sources and Resources Consulted
- All 15 `\bibitem` entries within the `thebibliography` environment
- Internal repository artifacts: frozen results, audit scripts, README files
- Standard terminology conventions in NLP, IR, and computational legal research

## C. Main Overlap Findings
No material unattributed textual overlap was identified within the sources examined.

Two categories of expected similarity were found:
1. Technical descriptions of the ILDC corpus share terminology with Malik et al. 2021 — expected and appropriate given that ILDC is the benchmark being described.
2. The BM25 ranking basis is described using standard IR terminology consistent with Robertson & Zaragoza 2009 — correctly cited.

## D. Standard-Terminology Exceptions
The following phrases are standard, unavoidable technical terminology and were preserved without modification:
- `TF--IDF unigrams/bigrams`, `Recall@5`, `Recall@100`, `macro-F1`
- `mean pooling of window logits`
- `InLegalBERT chunk-and-pool`
- `BM25`, `FTS5`, `SQLite`, `PostgreSQL`

Rewriting these would reduce precision without improving originality.

## E. Properly Cited Source-Derived Material
- The *Pooja Ramesh Singh v. Jammu and Kashmir Bank Ltd.* ruling (2026 INSC 668) is summarized accurately and attributed to the public Supreme Court PDF [poojasingh2026].
- InLegalBERT revision `b5ecfed8` is attributed to Paul et al. 2023 [paul2023].
- Tesseract OCR use is attributed to Smith 2007 [smith2007].

## F. Passages Rewritten for Clarity and Natural Voice
Several structurally template-like phrases were rewritten for scholarly quality (not for overlap reduction). Examples:
- "The central finding is a dissociation:" → "Our primary finding highlights a clear dissociation:"
- "We built and evaluated..." → "We designed, implemented, and evaluated..."
- "This paper treats that requirement as the design constraint:" → "We treat that constraint as the design foundation:"

No source-borrowed passages were identified that required rewriting for attribution reasons.

## G. Remaining Unavoidable Overlap
Structural similarity between the paper's methodology section and the repository's technical documentation is expected: the paper formally describes the same system. No attribution correction is required.

## H. Citation Audit
All `\cite{}` keys resolve to `\bibitem{}` entries. Verified:
- `poojasingh2026`: Supreme Court of India, 2026 INSC 668 — intact
- `taxflow2026`: DOI `10.1080/08839514.2026.2626097` — intact
- `smith2007`: Tesseract OCR — correctly associated with OCR corpus repair
- `dahl2024`, `nay2023`, `malik2021`, `paul2023`, `shukla2022`, `coliee2023`, `legalbench2023`, `casehold2021`, `casefacts2026`, `lextime2025`, `lewis2020`, `robertson2009`: all verified to match the claims they support

No citations were fabricated, altered, or invented. No metadata was changed.
