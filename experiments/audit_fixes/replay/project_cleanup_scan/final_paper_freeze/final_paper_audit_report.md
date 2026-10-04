# Final Paper Audit Report

**Generated:** 2026-09-29 (Updated Prompt 27 — final definitive)

---

## 1. Baseline State

| Item | Value |
|------|-------|
| Pre-edit TEX SHA-256 | `FADC2392166664C60FB18365557BF065123AD62DE476F81A94DA3FAC236F961C` |
| Pre-edit PDF SHA-256 | `93EECD93CBD2EA8D98266703E93D020B656C986858C282DC3326193F75EDB712` |
| Only manuscript source | `paper_master_final.tex` ✓ |
| No superseded manuscripts | Confirmed |

---

## 2. Files Modified

- `paper_master_final.tex` — scientifically frozen; Prompts 24/25/26/27 corrections applied
- `paper_master_final.pdf` — freshly rebuilt from updated `.tex` (Prompt 27)
- `originality_audit.md` — overclaiming corrected; explicit scope limitation added
- `humanization_edit_log.md` — updated with all edit hashes
- `claim_evidence_matrix.md` — fully rewritten to cover all numerical claims

---

## 3. Humanization Summary (Prompts 24 + 25)

| Location | Change | Meaning changed? |
|----------|--------|-----------------|
| Abstract | Scope narrowing, verified numbers only | No |
| Intro L85 | "This paper treats..." → "We treat that constraint as the design foundation:" | No |
| Conclusion L662 | "We built and evaluated..." → "We designed, implemented, and evaluated..." | No |
| Conclusion L675 | "acknowledged limitations" → "their limits" | No |
| Method L390 | Removed orphaned "combined 37 cases" | No |
| Results L438 | Fixed garbled 4-population sentence → clean 2-population statement | No |
| Limitations L612 | Removed "extended additively to 37" | No |

---

## 4. Scientific Claim Corrections Applied

| Claim | Action | Prompt | Reason |
|-------|--------|--------|--------|
| Extension-7 stratum | Removed | 24 | Not independently replayed |
| Combined-37 stratum and table rows | Removed | 24 | Not independently replayed |
| 14-case LLM presentation subsection | Removed | 25 | Exploratory; non-independent |
| `\subsection{Explanation format}` | Removed | 25 | Survival from Prompt 24 regex miss |
| `extended additively to 37` in Limitations | Removed | 25 | Orphaned reference |
| `combined 37 cases` in Method | Removed | 25 | Orphaned reference |
| `OCR restored 12 of 15...` exact count | **Removed** | **27** | HISTORICAL — not independently replayed |

---

## 5. E3/E4 Base-30 Outcome Evidence Classification

Evidence source: `validation_replay/e3_e4/e3_e4_reproduced_evaluation.json`

| Metric | Value | Status in replay JSON | Classification |
|--------|-------|-----------------------|----------------|
| E3-pred accuracy | 0.666667 | `EXACT_REPRODUCTION`, difference=0.0 | **VERIFIED_REPLAY** |
| E3-pred macro_f1 | 0.603175 | `EXACT_REPRODUCTION`, difference=0.0 | **VERIFIED_REPLAY** |
| E4-pred accuracy | 0.666667 | `EXACT_REPRODUCTION`, difference=0.0 | **VERIFIED_REPLAY** |
| E4-pred macro_f1 | 0.603175 | `EXACT_REPRODUCTION`, difference=0.0 | **VERIFIED_REPLAY** |

Numbers retained in paper. The `MINOR_NUMERICAL_DRIFT` flag on `per_case_stable_records` (5/30 cases differ in raw logits at ~1e-4 due to torch/cuDNN nondeterminism) does not affect any reported metric.

---

## 6. Citation Audit

All 15 `\bibitem` entries verified. Key entries:
- `poojasingh2026`: Supreme Court of India, 2026 INSC 668 — intact
- `taxflow2026`: DOI `10.1080/08839514.2026.2626097` — intact
- `smith2007`: Tesseract OCR — now cited in both Corpus section and Limitations

---

## 7. Scientific Claim Content Scan (Prompt 27)

**Forbidden terms — all 0:**

| Term | Count |
|------|-------|
| Combined-37 | 0 ✓ |
| Extension-7 | 0 ✓ |
| 14-case | 0 ✓ |
| LLM-based presentation | 0 ✓ |
| 99.20 | 0 ✓ |
| extended additively to 37 | 0 ✓ |
| combined 37 | 0 ✓ |
| OCR restored | 0 ✓ |
| IEEEtriggeratref | 0 ✓ |
| IEEEtriggercmd | 0 ✓ |
| enlargethispage | 0 ✓ |

**Required verified claims — all present:**

| Claim | Occurrences |
|-------|-------------|
| 0.61344 | 2 ✓ |
| 0.612342 | 2 ✓ |
| 12/30 | 5 ✓ |
| 15/30 | 4 ✓ |
| 150/150 | 4 ✓ |
| 0/150 temporal | 1 ✓ |
| ranking level | 2 ✓ |
| BM25 | 13 ✓ |
| poojasingh2026 | 3 ✓ |
| taxflow2026 | 3 ✓ |
| smith2007 | 4 ✓ |
| 0.666667 | 4 ✓ |
| 0.603175 | 4 ✓ |

---

## 8. LaTeX Build Results

| Item | Result |
|------|--------|
| Build method | Tectonic 0.15.0 static binary via `docker-desktop` WSL; cache at `C:\tectonic_build\tectonic_cache` |
| Build result | **SUCCESS** (exit 0) |
| Overfull boxes | **0** |
| Underfull boxes | 10 cosmetic (table cells, short paragraphs) — unchanged |
| Author block overflow | Fixed (Prompt 26: `\hspace{2.5em}` → `\hspace{1.0em}`, emails wrapped in `{\small ...}`) |
| No page hacks | ✓ |

---

## 9. Page Count

**EXACTLY 6 PAGES** — confirmed: `[1][2][3][4][5][6]88631 bytes written`

---

## 10. Final Manuscript Hashes (Prompt 27 — definitive)

| File | SHA-256 |
|------|---------|
| `paper_master_final.tex` | `8DD1AD3741980AA4BFDD24AE9DF6767B560826B7F223BA9766CE2B036FC16D2F` |
| `paper_master_final.pdf` | `BBE0EABAE42CA7ED09A115A7DFFDE54E5C1DFAD9E195F777CE6B3FF697E27309` |

---

## 11. Git Status

`paper_master_final.tex` and `paper_master_final.pdf` are **untracked** (`??`). Nothing committed per owner policy.

---

## 12. Remaining Notes

- `C:\tectonic_build\` contains the tectonic binary and cache — not a repository file; should be added to `.gitignore` or removed before submission.
- Underfull boxes in table cells are cosmetic; no visible clipping.

---

## 13. Final Readiness Classification

> ## ✅ READY

- [x] TEX is final (`8DD1AD37...`)
- [x] PDF freshly compiled (`BBE0EABA...`)
- [x] **Exactly 6 pages** (`[1][2][3][4][5][6]`)
- [x] **0 overfull hboxes**
- [x] Exact unverified OCR counts **removed**
- [x] E3/E4 Base-30 outcome numbers: **VERIFIED_REPLAY** — retained
- [x] All manuscript numerical claims covered in `claim_evidence_matrix.md`
- [x] All forbidden terms: **0**
- [x] All required verified claims: **present**
- [x] Citations resolve, references resolve
- [x] No artificial page-count hacks
- [x] Not committed (owner reviews before committing)
