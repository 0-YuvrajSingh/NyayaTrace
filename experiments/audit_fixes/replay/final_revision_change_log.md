# Final revision change log (paper_master_revised.tex → paper_master_final.tex)

Base: revised manuscript (11 pages, ~7,204 words) with all prior factual corrections retained
(1985_40 retrieved-only, 28+1+10 freeze count, scoped guarantee language, Pooja Singh
attribution pending verification, `\texttt{YYYY_N}` fix, fp16 + BM25-scope + 14-case
limitations, TypeScript-claim removal).

## Factual corrections / resolutions
| Location | Original issue | Revision | Evidence |
| -------- | -------------- | -------- | -------- |
| Abstract + Introduction + References | Pooja Singh holding cited to order copy with conflicting URL hash | Holding verified against the court's own publication: case name, 2026 INSC 668, Civil Appeal No. 11950 of 2025, decided 2 July 2026, NCLT + appellate judgments set aside over nonexistent/fake/AI-hallucinated material; bibliography now cites the sci.gov.in court PDF | sci.gov.in judgment PDF (2026 INSC 668, pp. 1–2); IBBI Supreme Court orders listing (entry 10, 02 Jul 2026, CA 11950/2025) |
| References (taxflow2026) | Co-authors as bare initials (N. S., M. M., H. V.), no DOI | Verified title/journal/vol.40(1)/art.2626097/year/DOI against publisher record; unverifiable author fragments replaced with honest `et al.`; DOI added | Taylor & Francis article page + ResearchGate record (DOI 10.1080/08839514.2026.2626097); full T&F page blocked (403), so no further author detail asserted |
| Error Analysis | 1985_40 "retrieved and selected" | Retrieved-only/rank 78 (three selected + one retrieved-only) | frozen per-case flags (retrieved=True, selected=False) |
| Reproducibility | "29 byte-exact" | 28 + 1 line-ending-normalized + 10 metadata-differing | week16 RR-01/RR-02 |
| Worked example | Passage-topic gloss not cross-checked | Gloss removed; rank-78 fact and illustration framing kept | citation audit (NOT VERIFIED) |

## Compression (no verified value altered; all section structures kept)
Removed: Fig.1 (Table II covers it), Fig.4, Fig.5 (numbers kept in text),
overlap table (values folded into prose: 684/238/213/368 + 18/3/3/6),
buckets table (partition + ranks kept in prose; full ID lists remain in frozen artifacts),
worked-example subsection, RQ3 itemize→paragraph, recovery/integrity itemize→paragraph,
privacy-deployment paragraph, demo description sentences, duplicate/unverifiable hedging.
Shortened: abstract, contributions, related work + positioning, corpus/OCR/alignment prose,
method subsections (config version IDs kept), protocol prose, results prose, table captions,
figure widths 0.80→0.62 (readability preserved), limitations bullets (all bullets kept),
governance (merged, transparency list kept short), conclusion, future work, reproducibility.
No font, margin, or spacing manipulation; all 15 references retained; no citation removed.

## Deliberately not changed (would require inventing evidence)
Remaining taxflow2026 author surnames; combined-37/extension/LLM/probe/OCR figures kept with existing
artifact/exploratory qualifiers; full per-case ID enumerations moved to artifacts only.

## Restructure to Base-30 verified core (review direction)
Abstract, central result, and conclusion reframed around independently replayed
Base-30 (12/30, 15/30, 150/150, 0/150, 0/30) instead of combined-37.
Extension-7/Combined-37 rows kept in Table III with an explicit
"reported, not replayed" caption; combined prose reduced to artifact-labeled clauses.
LLM numbers removed entirely (non-numeric exploratory statement only).
Positive-controls sentence removed. Probe history labeled as un-replayed development
record. Reproducibility "all metrics" broadened claim replaced with scoped replay
statement. Funnel/integrity figures removed (base evidence carried by tables).

## Final build
Revised: 11 pages, ~7,204 words. Final: 6 pages, 4,516 words.
pdflatex twice: success, no errors, no Overfull boxes, no undefined references/citations
(only Underfull-hbox warnings, left as-is).
pdflatex ×2: success, no errors, no undefined references/citations (only Underfull-hbox
warnings, left as-is). All cross-references via \ref (no hardcoded numbers).
Remaining tables: operational definitions, outcome, RQ1 strata, integrity.
No figures remain; tables carry all evidence. All 15 references retained.
Layout fixes: removed template trigger lines that forced a spurious 7th page;
restored breakable identifier forms (18pt/37pt overflows resolved);
residual-gap limitation reworded to the verified Base-30 figure.
