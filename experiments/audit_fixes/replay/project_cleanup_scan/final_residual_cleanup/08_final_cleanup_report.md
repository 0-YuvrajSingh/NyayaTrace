# Prompt 21 — Final Cleanup Report

**Prompt:** 21  
**Phase:** Final Residual Cleanup + Submission Manuscript Cleanup + TS Preservation  
**Executed:** 2026-09-29  
**Branch:** audit-fixes

---

## Executive Summary

| Category | Count | Action |
|----------|-------|--------|
| Active manuscripts remaining at root | 2 (`paper_master_final.tex` + `paper_master_final.pdf`) | KEEP_CANONICAL |
| Manuscript copies in submission/ | 2 (`submission/final/paper_master.tex/.pdf`) | BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE |
| Historical submission archive files | 6 (`submission/archive/*`) | KEEP_HISTORICAL_SUBMISSION_EVIDENCE |
| Legitimate TS/TSX/MJS assets preserved | 15 (8 src + 3 dist + 4 demo/*.mjs) | KEEP |
| Scratch scripts | 25 | KEEP_AUDIT_EVIDENCE (git-tracked) |
| Experiment audit/replay logs | 39 (31 logs/ + 7 replay-root + 2 project_cleanup_scan) | KEEP_AUDIT_EVIDENCE |
| Experiment scripts | 65 (`experiments/audit_fixes/scripts/`) | KEEP_AUDIT_EVIDENCE |
| Validation replay | 35 files (~154 MB) | BLOCKED_PROVENANCE_UNCLEAR |
| Safe deletions executed | 1 (empty `spec_clean/` directory) | EXECUTED |
| Blocked items (owner decision needed) | 2 files (`submission/final/paper_master.tex/.pdf`) | BLOCKED |

---

## Phase A — Manuscript Uniqueness

Exactly **2 `.tex` files** exist in the repository:
1. `paper_master_final.tex` (root) — `FADC2392...` — **KEEP_CANONICAL**
2. `submission/final/paper_master.tex` — `9DE053A7...` — **BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE**

Exactly **0 `.docx` files** remain (both deleted in Prompt 20).

No other manuscript source, backup, or draft exists outside `submission/`.

## Phase B — Submission Tree

The `submission/final/` package is a **cryptographically self-described historical submission package**:

- `MANIFEST.md` records SHA-256 of every component including `paper_master.tex` and `paper_master.pdf`
- `nyayatrace_submission_package.zip` (SHA `5F213D9F...` — verified against MANIFEST) **embeds** the superseded `paper_master.tex` + `paper_master.pdf` verbatim
- Deleting the loose `.tex/.pdf` while preserving the ZIP would leave the package in an internally inconsistent state (the ZIP contents would not be verifiable against surviving loose files)

**Decision: BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE** — no deletion without explicit separate owner authorization to retire the entire submission package.

The `submission/archive/` subtree is explicitly governed by `SUPERSEDED.md`, which documents the `git mv` provenance of each file. All 6 files are `HISTORICAL_SUBMISSION_EVIDENCE` — no action.

## Phase C — TypeScript/JavaScript

15 assets audited and preserved:
- 8 `demo/web/src/` TypeScript source files + configs + lockfile
- 3 `demo/web/dist/` Vite build outputs (retained intentionally)
- 4 `demo/*.mjs` git-tracked demo modules

Zero deletions.

## Phase D — Scratch

25 git-tracked JS/Python audit scripts. All classified `KEEP_AUDIT_EVIDENCE`. Zero deletions.

## Phase E — Experiments/Audit Fixes

65 Python/shell scripts in `experiments/audit_fixes/scripts/` — untracked but constituting the replay tooling. All `KEEP_AUDIT_EVIDENCE`.

39 log files across `replay/logs/`, `replay/` root, and `project_cleanup_scan/` — execution evidence for E1/E2/E3/E4 replay. All `KEEP_AUDIT_EVIDENCE`.

Root-level audit reports in `experiments/audit_fixes/` (8 files) — `KEEP_AUDIT_EVIDENCE`.

**1 deletion executed:** `experiments/audit_fixes/spec_clean/` — empty gitignored directory.

## Phase F — Validation Replay

`validation_replay/` (35 files, ~154 MB): **BLOCKED_PROVENANCE_UNCLEAR**

Owner instruction from Prompt 19 stands: "Do not delete validation_replay/ merely because it has no active references. Its independent replay provenance is still unresolved."

Classification unchanged. Zero modifications.

## Phase G — Global Residual

| Search category | Result |
|----------------|--------|
| Zero-byte files | **None found** |
| Editor artifacts (*.bak, *.tmp, *.swp, ~$) | **None found** |
| Temporary extraction dirs | **None found** |
| Duplicate configs | **None found** |
| Empty directories | **1 found** → `spec_clean/` → **DELETED** |
| Accidental exports | **None found** |
| Stale caches | `demo/web/dist/` → intentional, retained |

---

## Remaining Owner Decisions

### Decision 1 — `submission/final/paper_master.tex` + `paper_master.pdf`
**Status: BLOCKED_HISTORICAL_SUBMISSION_PROVENANCE**

These are load-bearing components of the historical submission package. The ZIP (`nyayatrace_submission_package.zip`) embeds both files, and `MANIFEST.md` cryptographically records their SHA-256.

To remove them, the owner would need to decide:
- **Option A:** Delete loose `.tex/.pdf` only (leaves ZIP + MANIFEST internally consistent but the directory-level files are gone — the ZIP still "contains" them)
- **Option B:** Delete the entire `submission/final/` directory (ZIP + loose files + figures + MANIFEST + README) — full retirement of the historical submission package
- **Option C:** Keep as-is (current state)

**The agent will not make this decision. Awaiting explicit owner authorization.**

### Decision 2 — `validation_replay/` (~154 MB)
**Status: BLOCKED_PROVENANCE_UNCLEAR**

Awaiting separate owner decision since Prompt 19. No change in this prompt.

---

## Cumulative Cleanup Totals (Prompts 19 + 20 + 21)

| Prompt | Files/items deleted | Bytes recovered |
|--------|---------------------|----------------|
| Prompt 19 | 8 files | 281,649 |
| Prompt 20 | 15 files | 2,088,696 |
| Prompt 21 | 1 directory (0 bytes content) | 0 |
| **Total** | **23 files + 1 empty dir** | **~2,370,345 (~2.26 MB)** |
