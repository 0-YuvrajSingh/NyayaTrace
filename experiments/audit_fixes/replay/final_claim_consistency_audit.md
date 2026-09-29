# Final claim consistency audit (revised manuscript)

Build: pdflatex ×2, success; no errors; no undefined references or citations;
only Underfull-hbox warnings (left as-is). All five figures rendered.
Revised PDF: 11 pages, ~7,204 words (original: 10 pages, ~7,077 words; +2 limitation
paragraphs and rewordings; no sections removed, nothing moved to supplementary).

## Verified quantitative claims (all preserved exactly)
E1 0.61344/0.612342, class F1 0.632975/0.591708, CM [[501,248],[333,421]];
E2 mean 0.596806/0.592358, vote 0.6015/0.5937, majority 0.5017/0.3341;
1517→14→1503; base Recall@5 12/30, Recall@100 15/30, provenance/groundedness 1.0,
precision 0.08 (ceiling 0.20); E3/E4 base 0.666667/0.603175 CM [[4,3],[7,16]];
combined 0.648649/0.607347 CM [[6,3],[10,18]] (artifact-labeled);
5391→11; 8927/1304/7623; era 5/13/9/2/1 (43.3%); 684/238/213/368 and 18/3/3/6;
checkpoint SHA 924a5bb9…dbdc773; 81/6/8 tests.

## Claims removed
- "passing TypeScript compile plus production frontend build" (unevidenced).
- Implication that 1985_40 was selected (now retrieved-only).
- Unconditional "guarantee" of no post-dating (now scoped).
- "29 byte-exact" (now 28 + 1 normalized + 10).

## Claims weakened/qualified
- Pooja Singh passages attributed to the cited order copy (×2).
- Positive controls marked "recorded".
- New fp16, BM25-scope, and 14-case-filter limitation statements.

## Remaining NOT VERIFIED (unchanged, disclosed in paper or logs)
LLM-rater numbers and self-review means (presentation-only qualifiers kept);
combined-37/extension figures (strata qualifiers kept); probe/OCR/99.2% process
figures; Pooja Singh holding and order-copy URL selection (external research needed);
taxflow2026 authorship and minor reference formatting; TypeScript evidence absent.
No new unsupported result was introduced; no validated value was altered.
