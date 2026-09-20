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
5. Kriti Mishra (kritimishra@akgec.ac.in)

Department of Computer Science and Engineering,
Ajay Kumar Garg Engineering College, Ghaziabad, India

## Mentorship and Guidance

- Kriti Mishra (Department of Computer Science and Engineering, AKGEC) — acknowledged in Section Acknowledgment

## Cryptographic Hashes (SHA-256)

- `paper_master.pdf`: `52d5ba9884818deb1186a104e278644f270bcfe2810003e9e069e5a9a1eff6af`
- `paper_master.tex`: `bcc60a3e6943f7037d575f1a0537245c2fcdeb1b0e43721437b416424dee65e0`
- `nyayatrace_submission_package.zip`: `80d16e35e5503acfe3095f401ad7f41ab0a5aa9cfe2c5b9fa77f9d451c905bdb`
- `figures/fig1_outcome.pdf`: `d4fc9fed87e7285128e215f30f5e08adefddfae50c9a927b029413e2096930bb`
- `figures/fig2_funnel.pdf`: `b8a7eb5c84d8657afd3906c75c30425811d99d8c962e8fd54107d3eb08f0ebcf`
- `figures/fig3_integrity.pdf`: `54f85085364947c8df5829a9152f6e419e2f793b3408cf20a9b4c47833ed129c`
- `figures/fig4_investigation.pdf`: `95a55ab8791698aa2ad78d3f3fbf861ce3d935f6fb63ff95700918c2b3960e79`
- `figures/fig5_explanation.pdf`: `4f62b79c71a2a2b682bf98cf2cac8a54e50f6a40d3b7b2306399c772b9c6a13e`

## Rebuild Instructions

To compile the paper from this self-contained directory using pdfTeX (TeX Live 2025):
```bash
pdflatex paper_master.tex && pdflatex paper_master.tex && pdflatex paper_master.tex
```
All figures are located in `figures/` relative to `paper_master.tex`. The bibliography is embedded directly within `paper_master.tex`. No external path dependencies or extra `.bib` files are required.

## Status

READY FOR VENUE-SPECIFIC SUBMISSION CHECK.
