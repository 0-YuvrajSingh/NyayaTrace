# Submission package

This directory is the hand-off bundle for the research prototype.

| File | Role |
| --- | --- |
| `research_paper.pdf` | Canonical six-page IEEEtran paper (compiled from `research_paper.tex`). |
| `research_paper.tex` | Canonical LaTeX source; the bibliography is inline (`thebibliography`). |
| `figures/*.svg`, `figures/captions.md` | Evaluation-plot deliverable (Figures A–E). The paper itself embeds no figures. Regenerate with `python scripts/build_week14_paper_figures.py`. |
| `MANIFEST.md` | Required-deliverable inventory mapping each deliverable to its location in the repository. |
| `declaration_template.md`, `certificate_template.md` | Neutral institutional templates with marked placeholders; replace them with institution-specific pages where required. |

Build and check from the repository root:

```powershell
.\tectonic.exe -X compile submission/research_paper.tex --outdir submission
python validate_final.py
```

No target venue is recorded in the repository, so no venue-specific format (for example DOCX) or anonymisation is applied. If the venue is double-blind, anonymise the author block and the code URL in `research_paper.tex` before submission.

The runnable demo remains in [`../demo/`](../demo/): the static frozen-artifact viewer (`python scripts/serve_week16_demo.py --port 8000` from the repository root) and the connected local stack (`compose.demo.yaml`).
