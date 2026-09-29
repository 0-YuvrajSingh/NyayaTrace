# Prompt 20 — Post-Cleanup Integrity Check

**Verdict: PASS (11/11 checks)**  
**Executed:** 2026-09-29  
**Branch:** audit-fixes

> [!NOTE]
> Two checks initially failed due to wrong file paths in the verification script — not due to actual data loss. Both were diagnosed and confirmed correct. See notes below.

---

## Check Results

| # | Check | Result | Detail |
|---|-------|--------|--------|
| 1 | `paper_master_final.tex` SHA-256 | ✅ PASS | `FADC2392166664C60FB18365557BF065123AD62DE476F81A94DA3FAC236F961C` — matches frozen baseline |
| 2 | `paper_master_final.pdf` SHA-256 | ✅ PASS | `93EECD93CBD2EA8D98266703E93D020B656C986858C282DC3326193F75EDB712` — matches frozen baseline |
| 3 | `retrieval/bm25.sqlite` SHA-256 | ✅ PASS | `3187F7FCE824EA8CCC5A26D908936CE4B78E81238289EA69348CB861350D65FB` — matches frozen baseline |
| 4 | Corpus PDF count | ✅ PASS | 39,068 files (unchanged) |
| 5 | Corpus parquet count | ✅ PASS | 74 files (unchanged) |
| 6 | All 15 deletion targets gone | ✅ PASS | 0 still present on filesystem |
| 7 | TypeScript assets present | ✅ PASS | All 8 `demo/web/` source files present |
| 8 | `submission/` tree intact | ✅ PASS | Key files including ZIP, MANIFEST, SUPERSEDED.md all present |
| 9 | `validation_replay/` untouched | ✅ PASS | `freeze_validation.json` + `e2_cache/train/input_ids.npy` present |
| 10 | `corpus_consolidation_manifest.json` present | ✅ PASS | At `artifacts/local_cleanup/corpus_consolidation_manifest.json` (1,972,043 bytes) |
| 11 | Git staged removals | ✅ PASS | `paper_master.tex` + `paper_master.pdf` staged via `git rm` |

---

## Diagnostic Notes

### Check 3 — BM25 Hash (initially reported FAIL)
- **Root cause:** Verification script hashed `experiments/audit_fixes/replay/bm25.sqlite` instead of the canonical `retrieval/bm25.sqlite`.
- **Finding:** `retrieval/bm25.sqlite` = `3187F7FC...` ✅ matches frozen baseline exactly.
- `replay/bm25.sqlite` has a different hash (`F2A70BC5...`) — this is expected; it was built independently during the E2 replay run and is not the protected canonical index.
- **Resolution:** PASS — canonical index unaffected.

### Check 10 — Corpus Consolidation Manifest (initially reported FAIL)
- **Root cause:** Verification script checked `corpus_consolidation_manifest.json` at repo root; actual path is `artifacts/local_cleanup/corpus_consolidation_manifest.json`.
- **Finding:** File present at correct location, 1,972,043 bytes.
- **Resolution:** PASS — manifest preserved and intact.

---

## Frozen Baseline Summary (All Confirmed Intact)

| Asset | SHA-256 | Status |
|-------|---------|--------|
| `paper_master_final.tex` | `FADC2392...` | ✅ VERIFIED |
| `paper_master_final.pdf` | `93EECD93...` | ✅ VERIFIED |
| `retrieval/bm25.sqlite` | `3187F7FC...` | ✅ VERIFIED |
| Corpus PDFs | 39,068 count | ✅ VERIFIED |
| Corpus parquets | 74 count | ✅ VERIFIED |

---

## Git State Note

`paper_master.tex` and `paper_master.pdf` are staged for removal via `git rm`. A `git commit` on the `audit-fixes` branch will record these removals in history. This is the expected outcome per the Prompt 20 directive. The files are already gone from the filesystem; no functionality is affected by whether or when the commit is made.

**Pending commit message (suggested):**
```
chore(cleanup): remove superseded manuscript variants (Prompt 20)

Removed per owner-approved Prompt 20 final cleanup:
- paper_master.tex (superseded by paper_master_final.tex)
- paper_master.pdf (superseded by paper_master_final.pdf)

All other manuscript variants removed as untracked files.
Canonical paper_master_final.* preserved at root.
```
