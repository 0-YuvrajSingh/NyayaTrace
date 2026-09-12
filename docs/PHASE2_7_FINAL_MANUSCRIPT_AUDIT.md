# Phase 2.7 — Final manuscript audit (claim-to-artifact)

Manuscript: `paper_master.tex` (IEEEtran, 11-page PDF via Tectonic 0.15.0;
only Underfull-hbox warnings, no undefined refs/citations). All 11 pages
raster-inspected: title/authors, abstract, tables (outcome/strata/integrity/
defs/overlap/buckets/related), figures (5 PDFs regenerated from artifacts),
equations ($Y_q$, $k{=}100$, $C$, $L_2$, $\kappa$), references (15 entries),
captions, page breaks — no cropping, overflow, or malformed pages.

## Claim table (spot-checked programmatically against PDF text + JSON)

| Manuscript claim | Location | Population | Artifact | Exact value | Verified? |
|---|---|---|---|---|---|
| E1 0.6134/0.6123 | Abstr., §Results, Tab outcome | N=1503 | e1_baseline_results.json | 0.61344/0.612342 | YES |
| E2 0.5968/0.5924 (+vote 0.6015/0.5937) | same | N=1503 | e2_chunk_pool_results.json | exact | YES |
| Base-30 R@5/R@100 12/30, 15/30 | §Results, Tab IV | Base-30 | rq1_results.json strata | exact | YES |
| Ext-7 R@5/R@100 0/7, 5/7 | §Results, Tab IV | Ext-7 | rq1_results.json strata | exact | YES |
| Combined R@5/R@100 12/37, 20/37 | Abstr., §Results, Tab IV, Fig 2 | N=37 | rq1_results.json | 0.324324/0.540541 | YES |
| E3 combined 0.6486/0.6073 CM [[6,3],[10,18]] | §Results, Tab IV | N=37 | rq1_results.json | exact | YES |
| Integrity 185/185, 0/185, 0/37 | Abstr., §Results, Fig 3 | 185 cites/37 cases | rq2_results.json | exact | YES |
| Probes 37/37 ×3 mutations | §Results | 37/case | rq2_results.json | exact | YES |
| RQ3 dims +1.75/+1.0/+2.48/+2.52/+1.98, overall +1.95 | §Results, Fig 5 | 14×4 | rq3_results.json | exact | YES |
| RQ3 56/56 preference; DeepSeek≡GPT disclosed | §Results | 56 prefs | rq3_results.json + report | exact | YES |
| E1/E2 CMs, overlap 684/238/213/368, buckets, ranks | §Error analysis | N=1503/30 | week12 + e3_e4_error_analysis | exact | YES |
| Corpus 7,593; 5,082/994/1,517; 39,069 PDFs; 2.34M/2.04M chunks; 5,391→11; 1,304/7,623 | §Corpus | corpus-wide | manifest/identity/dedup/cleaning | exact | YES |
| Exactly RQ1/RQ2/RQ3; no RQ4 (0 hits) | §Problem→RQ3 | — | canonical spec | exact | YES |
| Year-granular strict-< temporal; no day-level claim | §Problem, §Method, §Limits | — | temporal.py + freeze | exact | YES |
| Non-human RQ3; anomaly; bundled E4; English/SCI; semester; no production | §Results, §Limits, §Governance | — | rq3 notes/status; design audit | exact | YES |

## Remaining UNVERIFIED items

- Live-URL resolution of bibliography links (incl. the imported Pooja Singh
  order PDF URL): not browsed during this task.
- External peer review of the manuscript itself (out of scope).

## Remaining BLOCKERS

None. PDF builds cleanly; all claims verified; figures reproducible from
repo data via the logged matplotlib script.
