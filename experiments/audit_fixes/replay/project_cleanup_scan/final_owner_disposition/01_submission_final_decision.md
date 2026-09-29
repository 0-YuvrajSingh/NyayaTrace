# Decision 1 — Historical Submission Package: Final State

## Classification Applied: RETIRE_HISTORICAL_SUBMISSION_PACKAGE

**Authorization source:** Owner Prompt 22 (prior execution) — explicit instruction:
> "Delete old manuscript material when it is clearly a research-paper copy, including `submission/final/paper_master.tex`, `submission/final/paper_master.pdf` and the historical submission package: `submission/final/nyayatrace_submission_package.zip`, `submission/final/MANIFEST.md`, `submission/final/README.md`, `submission/final/figures/*`"

**Executed at:** 2026-09-29 during Prompt 22 (prior) execution.

---

## Verified Current State of `submission/`

| Path | Exists? | Disposition |
|------|---------|-------------|
| `submission/final/` | ❌ **GONE** | Entire directory retired — all 10 files deleted via `git rm` |
| `submission/final/paper_master.tex` | ❌ **GONE** | SHA `9DE053A7...` (349,978 bytes combined with .pdf) |
| `submission/final/paper_master.pdf` | ❌ **GONE** | SHA `3B35C279...` |
| `submission/final/nyayatrace_submission_package.zip` | ❌ **GONE** | SHA `5F213D9F...` (370,841 bytes) |
| `submission/final/MANIFEST.md` | ❌ **GONE** | SHA `F56D942A...` |
| `submission/final/README.md` | ❌ **GONE** | SHA `3E8951E0...` |
| `submission/final/figures/fig1–fig5.pdf` | ❌ **GONE** | 5 PDF figures (71,242 bytes total) |
| `submission/archive/` | ❌ **GONE** | Entire directory retired — 6 files deleted via `git rm` |
| `submission/archive/paper.md` | ❌ **GONE** | SHA `D38FBA73...` |
| `submission/archive/paper.html` | ❌ **GONE** | SHA `9F59363D...` |
| `submission/archive/paper.pdf` | ❌ **GONE** | SHA `6E75198B...` |
| `submission/archive/paper_draft.md` | ❌ **GONE** | SHA `199ADF90...` |
| `submission/archive/paper_audit_report.md` | ❌ **GONE** | SHA `54A3FE3C...` |
| `submission/archive/SUPERSEDED.md` | ❌ **GONE** | SHA `8239EED8...` |

## What Remains in `submission/`

| Path | Status | Role |
|------|--------|------|
| `submission/MANIFEST.md` | ✅ PRESENT | Project-level required-deliverable manifest (cross-refs E1-E4, corpus, scripts) |
| `submission/README.md` | ✅ PRESENT | Project tree documentation |
| `submission/certificate_template.md` | ✅ PRESENT | Institutional placeholder |
| `submission/declaration_template.md` | ✅ PRESENT | Institutional placeholder |
| `submission/figures/week14_figure_a–e.svg` | ✅ PRESENT (5) | **Canonical SVG figures** — surviving copies after `artifacts/figures/` deletion |

## Manuscript Uniqueness — Final Confirmed State

Exactly **one `.tex` file** exists in the repository: `paper_master_final.tex` (root).  
Exactly **zero `.docx` files** exist anywhere.  
No manuscript copies exist in `submission/` or anywhere else outside the canonical pair.

> [!IMPORTANT]
> Decision 1 is **RESOLVED**. The historical submission package was retired in its entirety, consistently, in the prior Prompt 22 execution. No further action is required or available.
