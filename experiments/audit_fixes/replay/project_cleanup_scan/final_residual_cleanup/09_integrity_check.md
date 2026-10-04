# Prompt 21 — Final Integrity Check

**Verdict: PASS (14/14 checks)**  
**Executed:** 2026-09-29  
**Branch:** audit-fixes

---

## Check Results

| # | Check | Result | Detail |
|---|-------|--------|--------|
| K1 | `paper_master_final.tex` SHA-256 | ✅ PASS | `FADC2392166664C60FB18365557BF065123AD62DE476F81A94DA3FAC236F961C` |
| K2 | `paper_master_final.pdf` SHA-256 | ✅ PASS | `93EECD93CBD2EA8D98266703E93D020B656C986858C282DC3326193F75EDB712` |
| K3 | Only canonical `.tex` active outside submission/ | ✅ PASS | 1 file: `paper_master_final.tex` — no other .tex files exist outside `submission/` |
| K4 | Zero `.docx` files anywhere | ✅ PASS | 0 found — all DOCX files removed in Prompts 20/21 |
| K5 | `retrieval/bm25.sqlite` SHA-256 | ✅ PASS | `3187F7FCE824EA8CCC5A26D908936CE4B78E81238289EA69348CB861350D65FB` |
| K6 | Corpus PDF count | ✅ PASS | 39,068 (unchanged) |
| K7 | Corpus parquet count | ✅ PASS | 74 (unchanged) |
| K8 | TypeScript/MJS assets present | ✅ PASS | All 12 checked assets present (8 src + 4 demo/*.mjs) |
| K9 | `validation_replay/` untouched | ✅ PASS | `freeze_validation.json` + `e2_cache/train/input_ids.npy` both present |
| K10 | Submission ZIP untouched | ✅ PASS | `nyayatrace_submission_package.zip` SHA = `5F213D9F...` matches MANIFEST.md record |
| K11 | `corpus_consolidation_manifest.json` present | ✅ PASS | At `artifacts/local_cleanup/` — 1,972,043 bytes |
| K12 | `spec_clean/` directory deleted | ✅ PASS | Empty gitignored dir confirmed absent |
| K13 | No credentials/secrets present | ✅ PASS | 0 `.db_env` / `.env` / `credentials.json` files found |
| K14 | E2 checkpoint `model.safetensors` present | ✅ PASS | Found at `artifacts/e2_chunk_pool_checkpoints_cached/` |

---

## Manuscript Uniqueness — Final State

| Location | File | SHA-256 | Classification |
|----------|------|---------|---------------|
| Root | `paper_master_final.tex` | `FADC2392...` | **KEEP_CANONICAL — only active manuscript source** |
| Root | `paper_master_final.pdf` | `93EECD93...` | **KEEP_CANONICAL — only active compiled PDF** |
| `submission/final/` | `paper_master.tex` | `9DE053A7...` | BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE |
| `submission/final/` | `paper_master.pdf` | `3B35C279...` | BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE |
| `submission/archive/` | `paper.pdf` | `6E75198B...` | HISTORICAL_SUBMISSION_EVIDENCE (pre-reorder Markdown-derived PDF) |

No `.docx` files exist. No other `.tex` files exist outside `submission/`.

---

## Open Owner Decisions

| Item | Classification | Blocking reason |
|------|---------------|-----------------|
| `submission/final/paper_master.tex` + `.pdf` (2 files, 349,978 bytes) | BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE | Load-bearing in submission package; ZIP embeds both; MANIFEST cryptographically records both. Requires explicit owner decision on whether to retire the historical submission package. |
| `validation_replay/` (35 files, ~154 MB) | BLOCKED_PROVENANCE_UNCLEAR | Owner hold from Prompt 19; independent replay provenance unresolved. |

---

## Unexpected Deletions: 0  
## Unexpected Modifications: 0  
## Active manuscripts remaining: 2 (`paper_master_final.tex` + `paper_master_final.pdf`)  
## Legitimate TS/TSX/MJS assets preserved: 15  
## Safe deletions executed (Prompt 21): 1 (empty `spec_clean/` directory)  
## Blocked historical artifacts: 2 files  
## Blocked provenance artifacts: 35 files (`validation_replay/`)
