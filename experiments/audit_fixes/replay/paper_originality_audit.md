# Originality audit (from read-only subaudit: normalized 8-gram sweep + manual reads; no files modified)

Scope: `paper_master.tex` vs repository docs (*.md, docs/, demo READMEs, artifacts drafts, submission/archive precursors) and the older `Indian_Legal_XAI.docx` (extractable, ~4,300 words).

Overall: NO finding meets REVIEW REQUIRED.

- Pooja Singh case description (~19 words verbatim) shared with submission/archive precursors: GENERIC/EXPECTED (same-author draft lineage, cited).
- Temporal-policy wording (~25 words) shared with archive precursors: GENERIC/EXPECTED (own method boilerplate).
- BM25 salient-terms/temporal + 100-phrase/80% rule (~30 words) shared with archive drafts and freeze records: GENERIC/EXPECTED (frozen config description necessarily repeated).
- Abstract opening vs archive abstract: semantic similarity with revision (paraphrase + added strata numbers): GENERIC/EXPECTED.
- RQ1–RQ3 sentences (~18–22 words each) overlap the docx spec (64 8-grams incl. RQ phrasing): GENERIC/EXPECTED (frozen scope authority; consistency required, not copying).
- Methods/results/corpus prose vs week11/week12/week14/week15 drafts (up to 135 8-grams in one file): GENERIC/EXPECTED (documented pipeline artifacts → drafts → manuscript; same-author lineage with provenance footers).
- Numeric/terminology overlap (metric values, 1503/30/37/185, config IDs, "strictly earlier than the query year" in 25 locations): GENERIC/EXPECTED (shared technical terminology and numbers are not plagiarism per instructions).
- External literature: 15/15 cited inline; no 8+ word verbatim match to any repo-held external full text (no external full texts in repo); related-work descriptions are paraphrases: NO MATERIAL OVERLAP FOUND (full external comparison not performed).
- Structure (Intro → Related → Problem → Corpus → System → Method → Protocol → Results → Error → Limits → Governance → Conclusion) mirrors archive precursor with reordering and added strata: expected revision, not a copy-pattern concern.

Rule applied throughout: similarity scores alone never trigger accusations; classifications use only NO MATERIAL OVERLAP FOUND / GENERIC/EXPECTED OVERLAP / REVIEW REQUIRED.
