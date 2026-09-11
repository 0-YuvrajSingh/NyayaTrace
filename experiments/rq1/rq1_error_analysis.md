# RQ1 error analysis (descriptive; observed categories only)

Base30 (frozen pattern preserved): 12 retrieved+selected (top-5); 3
retrieved-only-top-100 (1980_133 r15, 1981_55 r28, 1985_40 r78); 15 absent.
No temporal violations, duplicate failures, or provenance failures in any
displayed citation (150/150 checks passed).

Extension7 (new evidence):
- Bucket 2 (retrieved only in top-100): 5 — 1992_286 r14, 1993_90 r16,
  1990_256 r26, 1990_234 r32, 1990_324 r89. Expected authority present in
  candidates but displaced from top-5 display by higher-BM25 sources (same
  selection bottleneck seen in base30 retrieved-not-selected cases).
- Bucket 3 (absent at k=100): 2 — 1991_87 (Khardah), 1991_136 (Patankar).
  Both are distinguished-authorities: the query discusses the authority only
  to set it aside, so lexical overlap with the authority text is thin and
  BM25 does not surface it. No mechanism beyond this observation is claimed.
- Buckets 4–8: none observed. Zero temporally ineligible selections,
  zero duplicate/self-match flags, zero identity mismatches among retrieved
  matches, zero provenance mismatches (35/35 checks passed).

Combined37: 12 top-5 / 8 retrieved-only-100 (3 base + 5 ext) / 17 absent
(15 base + 2 ext). Integrity holds across strata (185/185 grounded and
provenance-valid, 0 violations, 0 unsupported).
