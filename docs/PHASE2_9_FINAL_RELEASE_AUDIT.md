# Phase 2.9 — Final Release Audit

## 1. Release State

- Branch `main`, HEAD `34a70d3`, tags `v4-baseline-reproduced`,
  `v5-final-submission`, remote `origin https://github.com/0-YuvrajSingh/NyayaTrace.git`.
- Tree was clean at start. Manuscript files: `paper_master.tex` (supplied,
  previously reconciled), `paper_master.pdf` (rebuilt here),
  `figures/fig1-5_*.pdf` (generated from artifacts), `submission/paper.*`
  (alternate md/html/pdf package). No `.aux/.log/.out/.toc`, no duplicate
  or stale tex/pdf variants, no caches.
- Classification: release files (tex/pdf/figures); supporting (experiments,
  answer_key, artifacts, config, src, submission package, docs audits);
  historical (week14 SVGs, draft paper, prior packets); temp/stale: none.

## 2. Manuscript

`paper_master.tex` (IEEEtran conference, 11-page PDF). Post-2.8 state
verified: combined-37 prediction wording (§Method + §Results + Table IV),
Table V unsupported 0-of-30-cases, all denominators labeled.

## 3. Scientific Consistency

Two parallel sweeps found zero artifact mismatches (all values exact or
correctly rounded: E1/E2 + CMs, base/ext/combined retrieval + prediction +
CMs, RQ2 rates + probes, RQ3 dims + unanimity, corpus/dedup/OCR counts,
week-11 deltas, error-analysis IDs) and zero scope violations (3 RQs, no
RQ4, no autonomy/production/significance/causality/correctness conflation;
RQ3 exploratory non-human with anomaly disclosed). One genuine correction
made here (see §7).

## 4. Population / Denominator Audit

Full-tex sweep: every /30 /37 /150 /185 /1503 /14 /56 occurrence carries
an explicit population; units verified (cases vs citations vs
model-test); Table V fixed; abstract/intro/conclusion denominators
explicit. No remaining ambiguity that could mislead a reviewer.

## 5. RQ / Scope Audit

Exactly RQ1/RQ2/RQ3 canonical; E1 contextual; prediction secondary;
provenance/prediction ≠ correctness; no autonomy/production claims;
unreviewed-significance absent; RQ3 non-human exploratory; temporal
strictly year-granular (`precedent_year < query_year`, same-year excluded).

## 6. Bibliography Verification

15/15 entries present and mutually cited (no orphans). Targeted entries
match print: poojasingh2026 (INSC 668, 2026, + repo-list URL imported
here), taxflow2026 (Karna et al., Appl. Artif. Intell. 40(1):2626097,
2026 — independently confirmed real), casefacts2026 (Putta et al., ACL
2026, pp. 17246–17265 — independently confirmed real). IBBI PDF URL
unreachable on fetch (404) — reachability only; metadata retained as
printed, flagged below.

## 7. Repository URL Verification

CORRECTED: tex pointed at `github.com/rishiraj103/...` (stale upstream
path, sole occurrence repo-wide); now points at the current remote
`github.com/0-YuvrajSingh/NyayaTrace`. PDF rebuilt and re-verified after.

## 8. Figure / Table Audit

Fig 1 (n=1,503 baselines), Fig 2 (combined-37 funnel 12/8/17), Fig 3
(combined-37 integrity 37/37, 185/185, 0/185, 0/37), Fig 4 (dev n=9 +
base-30 pre/post, explicitly historical), Fig 5 (14×4 LLM dims,
non-human-labeled) — all regenerated from live artifacts; captions, axes,
and prose verified. Tables IV (strata), V (base-labeled), outcome,
overlap, buckets, defs verified cell-by-cell. No decorative figures.

## 9. Reproducibility Audit

Freeze v4 covers all 14 canonical items. CORRECTED: tex claimed "43
reproducibility-freeze integrity checks" — no such count exists in any
artifact (known counts: 14/14 doc + 34/34 hashes); now reads exactly that
with Week-16 attribution. Other claims verified: 81 tests (75+6),
ckpt-6318 SHA, deterministic replay, machine-readable configs. No dataset/
checkpoint-bundling overclaim (gitignored large assets + hash record
correctly described).

## 10. PDF Build

Tectonic 0.15.0, 11 pages, 183,964 bytes. Only cosmetic Underfull-hbox
warnings; zero undefined references/citations, bibliography clean, all
figures render, no overflow. SUBSTANTIVE warnings: none.

## 11. Visual Inspection

All 11 pages raster-read: title/authors, abstract, tables, all 5 figures,
equations, references (incl. imported URL), captions, breaks — no
clipping, cropping, overflow, overlap, malformed glyphs, blank or
orphaned pages. Fig 4 label collision from the prior build fixed and
re-verified.

## 12. Release Hygiene

No API keys/credentials/tokens/.env/private URLs/absolute paths in tex or
figures (scanned; only benign "token" substrings meaning text tokens).
No large binaries added (PDFs are the publication figures/manuscript).
No temp build files in repo.

## 13. Venue Compliance

No target venue specified anywhere in the repo (IEEEtran conference
format only) → venue-specific compliance was not assessed. No anonymity
handling performed (author block pre-filled as supplied; ORCIDs not
invented).

## 14. Remaining Limitations

Descriptive N=37; additive post-freeze extension; single-authority
reference; year granularity; bundled E4; non-human RQ3 + duplicate-run
unanimity caveat; English/SCI/ILDC scope; semester prototype; no
production claim. All retained in-text (§Limits).

## 15. Remaining Unverified Items

Live-URL resolution of bibliography links (IBBI fetch 404 noted above);
external peer review (out of scope).

## 16. Remaining Blockers

None. The two genuine corrections in this phase (repo URL; "43 checks"
count) are applied and re-verified.

## 17. Final Verdict: RELEASE READY WITH DISCLOSED LIMITATIONS
