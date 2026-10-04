# Decision 2 — Validation Replay: Final Disposition

## Classification: KEEP_AUDIT_EVIDENCE

**Action: NO DELETION — preserve `validation_replay/` in full.**

---

## Inventory

| Metric | Value |
|--------|-------|
| Total files | 28 |
| Total size | 154,188,457 bytes (147 MB) |
| Directories | `e1/`, `e2/`, `e2_cache/` (train/validation/test), `e3_e4/` |

### File listing

| Path | Bytes | Role |
|------|-------|------|
| `asset_inventory.json` | 6,776 | Inventory of all assets in the validation run |
| `baseline_execution_metadata.json` | 1,714 | Execution policy — forbidden rewrites, frozen asset list |
| `freeze_validation.json` | 4,721 | EXACT_MATCH verification of corpus parquets + configs |
| `metric_comparison.json` | 11,755 | **Per-experiment EXACT_REPRODUCTION status** |
| `provenance_reload.json` | 252 | DB reload provenance (2M+ chunks, 306K duplicates skipped) |
| `e1/e1_reproduced_results.json` | 5,860 | E1 reproduced predictions |
| `e1/e1_reproduced_results.md` | 1,670 | E1 human-readable summary |
| `e2/e2_reproduced_predictions.json` | 213,928 | E2 independently computed predictions |
| `e2_cache/cache_manifest.json` | 201,582 | E2 cache manifest |
| `e2_cache/test/*.npy + metadata.json` | ~29.6 MB | E2 test split tokenized arrays |
| `e2_cache/train/*.npy + metadata.json` | ~103.8 MB | E2 train split tokenized arrays |
| `e2_cache/validation/*.npy + metadata.json` | ~18.7 MB | E2 validation split tokenized arrays |
| `e3_e4/e3_e4_reproduced_evaluation.json` | 1,426,956 | E3/E4 independently computed evaluation |

---

## Overlap Analysis with Primary Replay

| Item | Primary Replay | Validation Replay | Overlap? |
|------|---------------|-------------------|----------|
| E1 predictions | `replay/e1_test.json` | `e1/e1_reproduced_results.json` | **Parallel independent run — different file, same results** |
| E2 predictions | `replay/e2_test_predictions.json` | `e2/e2_reproduced_predictions.json` | **Parallel independent run** |
| E3/E4 evaluation | `replay/e3e4_replay.json` | `e3_e4/e3_e4_reproduced_evaluation.json` | **Parallel independent run** |
| E2 cache arrays | `replay/e2_cache/` | `validation_replay/e2_cache/` | **Independent second tokenization — different provenance** |

The validation_replay is **not a duplicate** of the primary replay — it is a second, independently executed run whose outputs happen to match (which is exactly what validates reproducibility).

---

## Reproducibility Claim Assessment

`metric_comparison.json` records for every metric in the paper:

| Experiment | Status | Difference |
|------------|--------|------------|
| E1 accuracy | `EXACT_REPRODUCTION` | 0.0 |
| E1 macro_f1 | `EXACT_REPRODUCTION` | 0.0 |
| E1 class_0_f1 | `EXACT_REPRODUCTION` | 0.0 |
| E1 class_1_f1 | `EXACT_REPRODUCTION` | 0.0 |
| E2 | `EXACT_REPRODUCTION` | 0.0 |
| E3/E4 | `EXACT_REPRODUCTION` | 0.0 |

This data **directly supports** the paper's reproducibility claims. The 147 MB of E2 cache arrays provide bit-level proof that the model tokenization is deterministic. Without `validation_replay/`, the independent verification layer is lost.

---

## Could reproducibility be demonstrated without it?

**Partially.** The primary replay in `experiments/audit_fixes/replay/` contains the canonical frozen results. A reviewer could re-run the experiments to verify them. However, `validation_replay/` proves that a second independent run already did so and achieved exact agreement — this is a stronger claim than "the results are reproducible in principle."

---

## Classification Rationale

| Test | Result |
|------|--------|
| Contains evidence for current paper results? | ✅ YES — EXACT_REPRODUCTION for all E1/E2/E3/E4 metrics |
| Is unique (not duplicated elsewhere)? | ✅ YES — independent run, different cache provenance |
| Has historical scientific/audit value? | ✅ YES — independent reproducibility proof |
| Active code references? | ❌ None — but policy explicitly says "Do NOT delete solely because there are no active code references" |
| Would deletion affect reproducibility claims? | ✅ YES — removes the independent verification layer |

**Final verdict: `KEEP_AUDIT_EVIDENCE`**

> [!NOTE]
> Decision 2 is **RESOLVED as KEEP**. No deletion. `validation_replay/` is preserved in its entirety as independent scientific reproducibility evidence for the current paper's experimental results.
