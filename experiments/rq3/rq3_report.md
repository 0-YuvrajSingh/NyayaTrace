# RQ3 Results — Exploratory LLM-Based Transparency Evaluation

## 1. Design

The RQ3 packet compared two presentation formats using the same underlying retrieved evidence for each case. Evaluators rated five transparency dimensions on a 1–5 scale and selected which display was easier to verify. The packet contained 14 cases. The structured/unstructured condition mapping was hidden during evaluation and applied only during aggregation.

Four evaluator runs were aggregated:

- Gemini
- Claude Sonnet 4.6
- DeepSeek
- GPT-5.6 Luna

This is **LLM-based exploratory evaluation**, not independent human evaluation.

## 2. Preference outcome

Across 4 evaluators × 14 cases = 56 forced preferences:

- Structured preferred: **56/56 (100%)**
- Unstructured preferred: **0/56 (0%)**
- Tie: **0/56 (0%)**

All four evaluators selected the same condition for every case.

## 3. Mean rubric scores

| Dimension | Structured | Unstructured | Difference |
|---|---:|---:|---:|
| Evidence linkage | 4.589 | 2.839 | +1.750 |
| Citation verifiability | 4.696 | 3.696 | +1.000 |
| Traceability | 4.643 | 2.161 | +2.482 |
| Explanation clarity | 4.732 | 2.214 | +2.518 |
| Transparency / inspectability | 4.643 | 2.661 | +1.982 |
| **Overall mean** | **4.661** | **2.714** | **+1.946** |

## 4. Evaluator-level overall means

| Evaluator | Structured | Unstructured |
|---|---:|---:|
| Gemini | 5.000 | 2.200 |
| Claude Sonnet 4.6 | 3.643 | 3.057 |
| DeepSeek | 5.000 | 2.800 |
| GPT-5.6 Luna | 5.000 | 2.800 |

## 5. Interpretation

The exploratory LLM evaluations consistently favored the structured presentation. The largest mean differences were in traceability, explanation clarity, and transparency/inspectability. The result supports the narrower claim that explicit issue/authority/evidence organization was judged easier to inspect in this blinded presentation comparison.

The result does **not** establish a human-rated transparency effect and should not be reported as human evaluation. It also does not test legal correctness.

## 6. Reproducibility / data handling

The evaluator outputs were kept as separate runs. DeepSeek and GPT-5.6 Luna happened to produce identical rating outputs in the supplied files; those runs were not silently collapsed.

See `rq3_case_results.csv` for the 112 display-level ratings and `rq3_preferences.csv` for the 56 forced preferences.
