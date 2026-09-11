# RQ2 report — provenance/citation-validation ablation (A=E3 vs D=full E4, N=37)

Question: do provenance-constrained selection + citation verification reduce
unsupported/unverifiable legal claims? Controlled change is post-selection
verification only (design audit: selection path identical; intermediates
B/C not separable — A and D only). E3 performs zero checks; E4 renders,
asserts grounding, and fail-closed verifies (any failure raises; no E4
output on violation). "Unsupported" = assertion failure (structural), never
prediction error or retrieval miss.

## Strata (D-condition primary metrics, exact numerators)

| Set | Grounded | Provenance | TempViol | Unsupp | D-rejected |
|---|---|---|---|---|---|
| base30 | 1.0 (30/30) | 1.0 (150/150) | 0.0 (0/150) | 0.0 (0/30) | 0 items / 0 cases |
| ext7 | 1.0 (7/7) | 1.0 (35/35) | 0.0 (0/35) | 0.0 (0/7) | 0 items / 0 cases |
| combined37 | 1.0 (37/37) | 1.0 (185/185) | 0.0 (0/185) | 0.0 (0/37) | 0 items / 0 cases |

A-condition: 0 checks performed by construction (no detection mechanism);
all 185 selected items flowed through unverified. D-condition accepted all
185 and changed no output vs A on live data.

## Sensitivity (positive controls, unchanged verifier)

Passage mutation → rejected 37/37. Authority mutation → rejected 37/37.
Backdated query year → rejected 37/37. The gates demonstrably fire; live
data simply contains no violations for them to catch.

## Predictions (secondary, equality expected and observed)

Combined37 E3 == E4 exactly: 0.648649 / 0.607347 [[6,3],[10,18]] (identical
inputs to the shared predictor). Prediction is not the RQ2 result.

## Reading

On the frozen 37-case reference-evidence set this configuration produces a
ceiling effect with limited discriminative power: D provides measurable
protection over A in mechanism (111/111 probes rejected, fail-closed
property) but live-data deltas are all zero, so no superiority magnitude
can be estimated here. No legal-correctness, completeness, production, or
generalization claim is made. RQ1 values are preserved separately and were
not overwritten or reused as conclusions.
