# Final paper artifact audit — HTML + PDF regenerated from paper.md

No source/model/experiment/key/config change. No new experiments. No
result changes. No commit/push.

## Generation method (no documented toolchain existed in-repo)

Only the prior audit's note ("no pandoc/wkhtmltopdf") existed. Used:
1. HTML: Python `markdown` 3.10.3 (stdlib-adjacent, already installed) with
   the `tables` extension — the sole non-core construct in the source
   (5 tables, 5 figures, 0 fences, 0 footnotes) — wrapped in the previous
   paper.html's own doctype/head/A4-print-CSS template, which was preserved
   byte-for-byte, plus closing `</body></html>`.
2. PDF: headless Microsoft Edge `--print-to-pdf --print-to-pdf-no-header`
   on the regenerated HTML (honors the template's `@page A4` CSS).
Exact commands are logged in the session record; generator scripts lived in
temp (`gen_html.py`) and were not added to the repo, per output scope.

## HTML generation: SUCCEEDED

`submission/paper.html` 57,514 → 61,947 bytes. Structure fidelity:
md headings (1/18/29) == html h1/h2/h3 (1/18/29); 5 tables; 5 figures.

## PDF generation: SUCCEEDED (with validation limitation)

`submission/paper.pdf` 386,292 → 381,379 bytes, timestamp newer than
paper.md (03:56 > 03:41). Valid `%PDF-1.4`, 18 pages. PDF text is
glyph-subset encoded, so raw/zlib text extraction finds no phrases;
validation instead via (a) same-engine screenshot of the HTML source
(title/abstract/tables/§5 three-RQ list visually confirmed), (b) verified
HTML wording checks below (the exact file the PDF was printed from
seconds later), (c) structural PDF validity. Residual limitation: no
character-level PDF text assertion possible locally.

## Critical wording checks (generated HTML, extracted)

- Old 4-RQ wording absent (0 "RQ4"; old "RQ1 - Outcome baselines" gone;
  old "E3/E4 do not return an outcome label" passages gone with the older
  revision content now correctly replaced by md §9.2/§11.2 text).
- Exactly the three canonical RQs present; "no fourth research question"
  present; E1 contextual ("does not itself answer RQ1") present; E2-vs-E3
  as RQ1 grounding comparison present; blinded-LLM-exploratory
  non-human sentence present; static-demo/efficiency/diagram limitation
  sentences present.
- Numbers/tables/figures/references: conversion is structural only; all
  values carried verbatim from paper.md (spot-checked 0.6134/0.6667,
  12/30, R@5/R@100 rows in tables 1:1).

## paper.md ↔ HTML / PDF consistency

Consistent by construction (same source, minutes apart). Note: the
regeneration also carries forward the older-revision→current-md content
delta the stale HTML predated (E3/E4 prediction sections) — intended,
since paper.md is the source of truth.

## Tests

75 passed, 0 failed (host subset; torch pair environment-limited as
established; documentation-only change).

## Remaining limitations

PDF character-level content unverified locally (see method above);
paper.html/pdf now track md but any future md edit re-stales them until
regenerated with the logged commands.
