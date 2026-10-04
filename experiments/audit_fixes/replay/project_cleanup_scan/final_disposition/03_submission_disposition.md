# submission/ Tree Disposition — Prompt 20

## Classification: KEEP_HISTORICAL_SUBMISSION_PACKAGE

**Decision applied:** Option 1 (Recommended) — Keep entire `submission/` tree as the canonical historical journal submission package.

**Rationale:**

The `submission/` directory is a fully git-tracked, structured journal submission package. It contains:

| Path | Content | Disposition |
|------|---------|-------------|
| `submission/final/nyayatrace_submission_package.zip` | Actual journal submission ZIP | KEEP — irreplaceable submission artifact |
| `submission/final/figures/fig1–fig5.pdf` | Canonical PDF figures for the paper | KEEP — canonical figure assets |
| `submission/final/paper_master.tex` | SUPERSEDED manuscript (SHA `9DE053A7...`) | KEEP in place — within submission package context, this is the paper-as-submitted; its presence here has archival provenance meaning distinct from the root-level stale copy |
| `submission/final/paper_master.pdf` | SUPERSEDED compiled PDF (SHA `3B35C279...`) | KEEP in place — same reasoning; submission-package provenance |
| `submission/final/MANIFEST.md` / `README.md` | Submission metadata | KEEP |
| `submission/archive/` | Historical drafts with `SUPERSEDED.md` marker | KEEP — already marked superseded; no action needed |
| `submission/archive/paper.html/.md/.pdf` | Draft conversion artifacts | KEEP — inside archive; already annotated |
| `submission/archive/paper_audit_report.md` | Audit trail | KEEP — audit provenance |
| `submission/figures/week14_figure_*.svg` | SVG copies of canonical figures | KEEP — git-tracked canonical copies (note: artifacts/figures/ copies were deleted in Prompt 19 as redundant; submission/figures/ copies are the surviving canonical set) |
| `submission/MANIFEST.md` / `README.md` | Top-level submission docs | KEEP |
| `submission/certificate_template.md` / `declaration_template.md` | Submission form templates | KEEP |

## Key Distinction: Root vs. submission/final/

| Location | SHA-256 | Role | Prompt 20 action |
|----------|---------|------|-----------------|
| Root `paper_master.tex` (deleted) | `9DE053A7...` | Stale working copy at root | DELETED — approved by owner |
| `submission/final/paper_master.tex` (kept) | `9DE053A7...` | Paper-as-submitted at time of submission | KEPT — submission package provenance |

The bytes are identical, but the semantic role is different: the root copy was an uncontrolled stale working file; the `submission/final/` copy is the historically fixed paper-as-submitted. This distinction is preserved.

## validation_replay/ Disposition

**Classification: BLOCKED_PROVENANCE_UNCLEAR**

Owner explicitly instructed (Prompt 19): *"Do not delete validation_replay/ merely because it has no active references. Its independent replay provenance is still unresolved."*

No action taken. Status remains `BLOCKED_PENDING_SEPARATE_OWNER_DECISION`.

Contents: 35 files, ~154 MB (E1/E2/E3/E4 reproduced results + E2 cache arrays + manifest JSONs).

## scratch/ Disposition

**Classification: KEEP_GIT_TRACKED**

25 JS/Python one-off audit scripts are git-tracked. Per Prompt 20 TypeScript preservation policy and general policy against deleting tracked files without explicit approval, these are preserved as-is.
