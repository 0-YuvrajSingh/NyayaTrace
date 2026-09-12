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
- Build Toolchain: Tectonic 0.15.0 (XeTeX-compatible engine)

## Authors and Affiliations

1. Yuvraj Singh (yuvraj2312026@akgec.ac.in)
2. RishiRaj Jaiswal (rishi2312003@akgec.ac.in)
3. Rahul Ranjan (rahul2312151@akgec.ac.in)
4. Saurav Kumar Chaudhary (saurav2312023@akgec.ac.in)
5. Kriti Mishra (kritimishra@akgec.ac.in)

Department of Computer Science and Engineering,
Ajay Kumar Garg Engineering College, Ghaziabad, India

## Cryptographic Hashes (SHA-256)

- `paper_master.pdf`: `f06ed1df0d851dae02ca5e3951989192a319818236ef39d6e816dd86044ee01a`
- `paper_master.tex`: `39f302010726a1038c7da54c45d0d111e706cdbefece65f67a0b652e27151d57`
- `nyayatrace_submission_package.zip`: `b61fd50976aa950d325689feacb349be2e905b5eefb15ce69b442f33f1ad3616`
- `figures/fig1_outcome.pdf`: `9e3207b7db76831828ad8aff4aa7cfa15fd4b7bb5ce9ab923ccf96f77b677d08`
- `figures/fig2_funnel.pdf`: `f3b50afd21b1dae3ef21f875f971991788adc51e682fbe433b2499b7ef95af64`
- `figures/fig3_integrity.pdf`: `7de53a3b1a6e36599c3476614ca11500b80366df3e6b8722500f3c5fb494c369`
- `figures/fig4_investigation.pdf`: `4ce9422de8fb5e34a03dca5e22c83e8718f568214904afa07146744afee61c5e`
- `figures/fig5_explanation.pdf`: `8db538d64d743292a2df6591e263596255e5a16372ceb2431dcc1dea7dcbd08d`

## Rebuild Instructions

To compile the paper from this self-contained directory:
```bash
tectonic paper_master.tex
```
Or using standard TeX Live / pdflatex / xelatex:
```bash
pdflatex paper_master.tex && pdflatex paper_master.tex
```
All figures are located in `figures/` relative to `paper_master.tex`. The bibliography is embedded directly within `paper_master.tex`. No external path dependencies or extra `.bib` files are required.

## Status

READY FOR VENUE-SPECIFIC SUBMISSION CHECK.
