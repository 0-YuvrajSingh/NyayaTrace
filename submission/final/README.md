# NyayaTrace — Final Submission Package

This directory contains the self-contained publication package for the paper:
**"Temporally Constrained, Provenance-Verified Evidence Retrieval for Indian Legal Research"**

## Package Structure

- `paper_master.pdf`: Final compiled 10-page IEEEtran PDF.
- `paper_master.tex`: Complete LaTeX source (IEEEtran format with embedded bibliography).
- `figures/`: Vector PDF figures (1 through 5) referenced in the paper.
- `nyayatrace_submission_package.zip`: Compressed archive containing the PDF, TeX source, and figures for direct submission upload.
- `MANIFEST.md`: Detailed manifest with metadata, author details, and cryptographic SHA-256 hashes.

## Compilation

The package is fully self-contained. To rebuild using Tectonic:
```bash
tectonic paper_master.tex
```

## Details

- **Format:** IEEEtran conference (`\documentclass[conference]{IEEEtran}`)
- **Length:** 10 pages
- **Research Questions:** 3 canonical RQs (RQ1, RQ2, RQ3)
- **References:** 15 items embedded via `\begin{thebibliography}`
- **Figures:** 5 PDF figures
- **Tables:** 6 tables
