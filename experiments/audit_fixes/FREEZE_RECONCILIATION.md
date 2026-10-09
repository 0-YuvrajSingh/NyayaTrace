# Freeze Manifest Reconciliation

## Corpus Record Count Reconciliation
| Source | Reported Count | Reason for Difference |
|---|---|---|
| Frozen Baseline Specification (`config/reproducibility_freeze.json`) | 2,343,435 | N/A (Baseline) |
| Paper manuscript (`paper_master.tex`) | 2,343,435 | N/A |
| Cleaned-corpus JSONL verification | 2,343,435 | N/A |

**Quoted Number**: The paper should quote **2,343,435** records.
**Verification Command**: `find /repo/corpus/ecourts/cleaned/ -name '*.jsonl' | xargs wc -l | tail -n 1`
**Execution Date**: 2026-09-28

## Status Counts in Freeze Files

### 1. `config/reproducibility_freeze.json`
- **Total Paths Hashed**: 43 entries
*(This file records the baseline configuration and file hashes, but does not use 'status' fields).*

### 2. `validation_replay/freeze_validation.json`
- **Total Entries**: 30
- **EXACT_MATCH**: 22
- **BYTE_DRIFT**: 8
