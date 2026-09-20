# Final Submission Manifest — NyayaTrace

- Active Manuscript: `paper_master.tex`
- Active PDF: `paper_master.pdf`
- Format: IEEEtran conference (`\documentclass[conference]{IEEEtran}`)
- Page Count: 10 pages (US Letter, 612 x 792 pt)
- Research Questions: Exactly 3 canonical RQs (RQ1, RQ2, RQ3)
- Evaluated Population: 37-case reference evidence set (30 base + 7 verified extension)
- Displayed Citations: 185 citations across 37 cases (100% verified, 0 unsupported claims)
- Figures Count: 5 vector PDF figures (`figures/fig1_outcome.pdf` through `figures/fig5_explanation.pdf`)
- Tables Count: 6 result tables (TABLE I through TABLE VI)
- References Count: 15 embedded references ([1] through [15])
- Build Toolchain: pdfTeX 1.40.26 (TeX Live 2025/dev/Debian)

## Authors and Affiliations

1. Yuvraj Singh (yuvraj2312026@akgec.ac.in)
2. RishiRaj Jaiswal (rishi2312003@akgec.ac.in)
3. Rahul Ranjan (rahul2312151@akgec.ac.in)
4. Saurav Kumar Chaudhary (saurav2312023@akgec.ac.in)

Department of Computer Science and Engineering,
Ajay Kumar Garg Engineering College, Ghaziabad, India

## Faculty Mentorship and Guidance

- Kriti Mishra (Department of Computer Science and Engineering, AKGEC) — acknowledged in Section Acknowledgment

## Cryptographic Hashes (SHA-256)

- `paper_master.pdf`: `bb6ef314bdf0f4ab4e8899094ef4e90d76e58b0faa9f18ad738d3e4a7ed8cd7d`
- `paper_master.tex`: `bcc60a3e6943f7037d575f1a0537245c2fcdeb1b0e43721437b416424dee65e0`
- `nyayatrace_submission_package.zip`: `012c28baae51dd687da1eca5020130a3738a9d8d13970bd3a08944ea9f5221b4`
- `figures/fig1_outcome.pdf`: `6a2c7776ed817ec4b595fd93d5bd26d61df3b38692d0495e0dfa60c8179844a2`
- `figures/fig2_funnel.pdf`: `02287ec1da8ea1bc95d725a6cc211353535f82b781c1d06d1a309aeb414369cc`
- `figures/fig3_integrity.pdf`: `34965becf10f273a968d5408087ccc3c7de7f82de2da28a422eb41400e597432`
- `figures/fig4_investigation.pdf`: `3f4f97203b8173b91a67e8fa4620d266f6782d20ad50eb2e9f32c58214106d41`
- `figures/fig5_explanation.pdf`: `cc457a5efd28988ce0e3eb8ca6e4c2c364087aea9b90be2fda863dbea6d9c25e`

## Rebuild Instructions

To compile the paper from this self-contained directory using pdfTeX (TeX Live 2025):
```bash
pdflatex paper_master.tex && pdflatex paper_master.tex && pdflatex paper_master.tex
```
All figures are located in `figures/` relative to `paper_master.tex`. The bibliography is embedded directly within `paper_master.tex`. No external path dependencies or extra `.bib` files are required.

## Status

READY FOR VENUE-SPECIFIC SUBMISSION CHECK.
