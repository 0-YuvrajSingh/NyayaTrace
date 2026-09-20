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

- `paper_master.pdf`: `20da7444fd1ec289bcb72728447211b5edf82b10521f680a7678f46fb421d661`
- `paper_master.tex`: `bcc60a3e6943f7037d575f1a0537245c2fcdeb1b0e43721437b416424dee65e0`
- `nyayatrace_submission_package.zip`: `ebad2ef983122ef3f41be471fb59ab7eef6558cd3d9ae73045fd5e137ab9534d`
- `figures/fig1_outcome.pdf`: `993811b286422d4552908153312bd6d96aea1bcd2abacde9fc6fc508427589f2`
- `figures/fig2_funnel.pdf`: `37847d87430c7edc21f84631e26c1db2ae67c95f1101597e9797d5b364354119`
- `figures/fig3_integrity.pdf`: `efffabc3af0225aa23a4263ea14c31f61c47062f22092fd12669ecbc8d913e79`
- `figures/fig4_investigation.pdf`: `6582f864b915223524cf79adf02e092f6b66635432a66fb31308dbba68d8f720`
- `figures/fig5_explanation.pdf`: `c1abbe74f2bbf3e53c9792abcc4a9b1d59349ed3f5291e08dd041e0e30abb6af`

## Rebuild Instructions

To compile the paper from this self-contained directory using pdfTeX (TeX Live):
```bash
pdflatex paper_master.tex && pdflatex paper_master.tex && pdflatex paper_master.tex
```
Or using Tectonic:
```bash
tectonic paper_master.tex
```
All figures are located in `figures/` relative to `paper_master.tex`. The bibliography is embedded directly within `paper_master.tex`. No external path dependencies or extra `.bib` files are required.

## Status

READY FOR VENUE-SPECIFIC SUBMISSION CHECK.
