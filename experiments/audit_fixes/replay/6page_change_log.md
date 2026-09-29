# 6-page change log (paper_master_final.tex → paper_master_6page.tex)

Base: 7-page final (7 pages, 4,663 words). No verified numerical result was changed.

Scope note: Fig.1/4/5, overlap/buckets tables, and the worked-example subsection
were removed during the earlier 11→7-page pass (recorded in
revision_change_log.md / the 7-page build); this log covers the 7→6-page pass,
which used textual compression, caption shortening, one shared affiliation
block, and figure widths 0.80→0.58 only.

| Location | Content removed/compressed | Reason | Scientific impact |
| -------- | -------------------------- | ------ | ----------------- |
| Abstract | Rewrote opening as two crisp sentences; trimmed finding transitions | Length | None; all three findings + 56/56 kept |
| Introduction | Compressed fluency paragraph, Pooja paragraph verbs, design-constraint list, contribution items | Length | None; verified details (INSC 668, CA number, date) kept |
| Related Work | Merged clauses; dropped repeated endpoint nouns | Length | None; all 8 citations kept |
| Positioning | Shortened per-work boundary sentences | Length | None; distinctions kept |
| RQs | Compressed to three tight questions | Length | None; comparisons intact |
| Corpus | Tightened ILDC/eCourts/OCR/alignment/answer-key sentences | Length | None; all counts kept |
| System Design | Already compact; minor trims | Length | None |
| Method (E1/E2/E3/E4) | Compressed hyperparameter/config prose; config version IDs kept | Length | None; all settings kept |
| Protocol | Trimmed chunk-record sentence | Length | None; four states + results kept |
| Results | Compressed outcome/equality/combined/funnel prose | Length | None; all metrics kept |
| Retrieval mechanism | Parenthetical probe pathway | Length | None; 0/9→7/9 and deltas kept |
| RQ3 explanation | Headline-style rewrite; rater names folded | Length | None; 56/56 + deltas + qualifiers kept |
| Error Analysis | Headline rewrites; overlap values folded into prose (table removed); buckets partition kept in prose (table removed); "No correct prediction…" sentence removed | Length | Values preserved in prose; full ID lists remain in frozen artifacts |
| Limitations | Compressed all bullets; all bullets retained | Length | Wording tightened only |
| Governance | Merged to one paragraph; privacy-deployment paragraph removed | Length | Deployment scope still excluded ("not an adjudicator", loopback removed with demo sentence — demo tests sentence kept in Reproducibility) |
| Conclusion | Headline rewrites; future-work items shortened | Length | None; all findings kept |
| Reproducibility | Compressed to essentials; GitHub link kept | Length | None; 81/14/14/39/28+1+10/8/8/6/6 kept |
| Tables | Captions shortened (outcome, rq1strata, integrity, defs); overlap + buckets tables removed with values in prose | Length | None; 4 tables remain |
| Figures | Fig.1/4/5 already removed in 7-page version; Fig.2/3 widths 0.80→0.62 | Length | Readability preserved; all plotted numbers in text/tables |
| References | Pooja Singh verified citation; taxflow2026 DOI + et al.; all 15 entries retained | Audit compliance | Improved accuracy |

Removed sentences worth noting: "No correct prediction was accompanied by an unsupported citation"
(integrity table's 0/30 unsupported-claims row carries the same fact); privacy-deployment
paragraph (deployment exclusion retained in scope-adjacent sentences); worked-example
subsection (already removed in 7-page version).

## Final build
6 pages, 3,720 words (from 7 pages / 4,663). pdflatex x2 clean. Paragraphs removed: 9 subsections/blocks (3 figures, 2 tables, worked example, itemize blocks, privacy + demo paragraphs); paragraphs merged: ~25; figures/tables removed: 3 figures + 2 tables (values in prose/artifacts); verified values changed: 0.
