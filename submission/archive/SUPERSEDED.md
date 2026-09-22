# SUPERSEDED — Markdown submission artifacts (frozen, unedited)

The three files in this directory are the pre-reorder Markdown submission
artifacts, moved here unmodified (via `git mv`, history preserved) after the
IEEE manuscript was brought into citation-order compliance:

- `paper.md`, `paper.html`, `paper.pdf` — Markdown paper, its derived HTML,
  and the Edge-rendered PDF, all using the previous reference numbering
  (e.g. Pooja Singh as [6], Dahl et al. as [13]).

They are superseded by the actively maintained IEEE manuscript at the
repository root:

- `paper_master.tex` — references reordered into order of first citation
  (IEEE requirement; entry texts moved verbatim), duplicated freeze-audit
  sentence removed, last-page column balancing added, plus the two
  reviewer-clarity wordings (abstract 254→249 words; ILDC expanded at first
  body use). No numbers, results, RQs, methods, limitations, or conclusions
  were altered.
- `paper_master.pdf` — recompiled from that source (10 pages); verified with
  zero errors, zero undefined references, and a page-by-page visual read.

The current submission package is `submission/final/` (IEEE PDF + TeX +
figures + zip, with recomputed SHA-256 hashes in its `MANIFEST.md`).

Do not edit the archived files. They are retained solely so the numbering
change and the demo-description update (`paper.md:326`) remain traceable.

## Batch 2026-09-23 — pre-submission cleanup (approved)

Moved here unmodified (via `git mv`, history preserved) under Document 3's
governance principle (discarded material preserved, not erased):

- `artifacts/paper_draft.md` → `submission/archive/paper_draft.md`
  (superseded manuscript draft; no live references).
- `scratch/paper_audit_report.md` → `submission/archive/paper_audit_report.md`
  (Sep-21 audit-session findings narrative; no live references; the underlying
  checks live on as the `scratch/*.js` probes, retained separately).
