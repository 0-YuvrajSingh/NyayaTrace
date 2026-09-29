# 6-page claim check (paper_master_6page.tex → 6-page PDF)

Build: pdflatex ×2, success; no errors; no undefined references/citations.
Pages: exactly 6 (261 words on p6, all bibliography — substantive, not filler).
Visual: 4 tables (definitions, outcome, RQ1 strata, integrity), 2 figures
(funnel, integrity), all equations, captions, and references render; no clipping,
overflow, or orphaned headings observed in text extraction; standard IEEEtran
formatting throughout (no font/margin/spacing manipulation).

## Verified quantitative claims retained (values unchanged)
E1 0.61344/0.612342; E2 0.596806/0.592358, vote 0.6015/0.5937, majority
0.5017/0.3341; 7593 (5082/994/1517) → 14 excluded → 1503; 39069/39066 PDFs;
2343435/2036981 chunks; 5391→11; 8927/1304/7623; 20/9/1 audit → 1 relink + 9
replace, 30/30; era 5/13/9/2/1 (43.3%); extension IDs + 3 held back; base
Recall@5 12/30, Recall@100 15/30 (12+3, 15 absent); integrity 150/150, 0/150,
0/30, 3000 implicit; combined 12/37, 20/37, 185/185; precision 0.08
(ceiling 0.20), F1 0.133; E3/E4 0.666667/0.603175 [[4,3],[7,16]], combined
0.648649/0.607347 [[6,3],[10,18]]; extension 0/7, 5/7, ranks 14/16/26/32/89;
probe 0/9→7/9; 2013_35: 79; 1980_105: 3, top-5; 1985_40: rank 78;
684/238/213/368 + 18/3/3/6; 1974_36 + 1984_136 corrections; 56/56 with all
deltas and 4.66/2.71; self-review 7/7; checkpoint SHA; 81/14/14/39/28+1+10;
8/8 Spring, 6/6 FastAPI; 75–100 future key.

## Claims reworded during compression (meaning preserved)
Headline-style Findings; merged scope/RQ/corpus/method/results sentences;
caption shortenings; figure widths 0.80→0.58 (legible; all values in text);
shared single affiliation block (all authors same department).

## Claims removed
Fig.1/4/5 (data in tables/text); overlap + buckets tables (values in prose;
full ID lists in frozen artifacts); worked-example subsection (rank fact kept);
"No correct prediction…" sentence (0/30 row carries it); privacy-deployment
paragraph; demo description; duplicate hedging.

## Artifact-only results still qualified
Combined-37/extension ("later expanded analysis", strata); LLM numbers
("exploratory", "explicitly not human evaluation", "presentation evidence only");
 probe pathway ("development probe" vs "held-out"); positive controls
("recorded"); OCR process figures; Pooja Singh (verified court citation);
 taxflow2026 (DOI + et al.).

## Wording constraints confirmed
1985_40 retrieved-only; 28+1+10 freeze count; E3/E4 identical
decisions/metrics/evidence + fp16 note, never byte-identical; BM25 ranking-level
on evaluated queries only; leakage stated as mechanisms + 0-violation results,
never universal; guarantees scoped to fail-closed/metadata; no human-preference,
SOTA, superiority, proof, or TypeScript claims.

## NOT VERIFIED items (unchanged, disclosed)
LLM-rater and self-review numbers (no replay); combined/extension figures (no
replay); probe/OCR process figures (no replay); remaining taxflow2026 surnames.
No unsupported claim was introduced; no verified value was changed.
