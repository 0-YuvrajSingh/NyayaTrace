# Claim-Evidence Matrix

**Updated:** 2026-09-29 (Prompt 27 — OCR fix + E3/E4 verification)

Evidence source: `validation_replay/e3_e4/e3_e4_reproduced_evaluation.json` and `validation_replay/e2/e2_reproduced_predictions.json`

All entries marked `VERIFIED_REPLAY` have `"status": "EXACT_REPRODUCTION"` (difference = 0.0) in the replay JSON unless otherwise noted.

---

## Section: Outcome Prediction (1,503-case population)

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| E1 Accuracy | 0.61344 | `metric_comparison.json` E1 accuracy | VERIFIED_REPLAY |
| E1 Macro-F1 | 0.612342 | `metric_comparison.json` E1 macro_f1 | VERIFIED_REPLAY |
| E2 mean-logit Accuracy | 0.596806 | `metric_comparison.json` E2 mean-logit accuracy | VERIFIED_REPLAY |
| E2 mean-logit Macro-F1 | 0.592358 | `metric_comparison.json` E2 mean-logit macro_f1 | VERIFIED_REPLAY |
| E2 majority-vote Accuracy | 0.6015 | `metric_comparison.json` E2 majority-vote accuracy | VERIFIED_REPLAY |
| E2 majority-vote Macro-F1 | 0.5937 | `metric_comparison.json` E2 majority-vote macro_f1 | VERIFIED_REPLAY |
| Majority-class Accuracy | 0.5017 | `metric_comparison.json` majority-class baseline | VERIFIED_REPLAY |
| Majority-class Macro-F1 | 0.3341 | `metric_comparison.json` majority-class baseline | VERIFIED_REPLAY |
| E2 agreement: both correct | 684 / 1503 | `e2_reproduced_predictions.json` confusion matrix | VERIFIED_REPLAY |
| E2 agreement: both wrong | 368 / 1503 | `e2_reproduced_predictions.json` confusion matrix | VERIFIED_REPLAY |
| E1 only correct | 238 | `e2_reproduced_predictions.json` confusion matrix | VERIFIED_REPLAY |
| E2 only correct | 213 | `e2_reproduced_predictions.json` confusion matrix | VERIFIED_REPLAY |

---

## Section: E3/E4 Base-30 Outcome Prediction

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| E3-pred Base-30 Accuracy | 0.666667 | `e3_e4_reproduced_evaluation.json` → `E3-pred / accuracy` | **VERIFIED_REPLAY** |
| E3-pred Base-30 Macro-F1 | 0.603175 | `e3_e4_reproduced_evaluation.json` → `E3-pred / macro_f1` | **VERIFIED_REPLAY** |
| E4-pred Base-30 Accuracy | 0.666667 | `e3_e4_reproduced_evaluation.json` → `E4-pred / accuracy` | **VERIFIED_REPLAY** |
| E4-pred Base-30 Macro-F1 | 0.603175 | `e3_e4_reproduced_evaluation.json` → `E4-pred / macro_f1` | **VERIFIED_REPLAY** |
| E3 = E4 identical (no evidence rejected) | True | `e3_e4_reproduced_evaluation.json` → identical confusion matrices | **VERIFIED_REPLAY** |

> [!NOTE]
> 5/30 cases differ in raw `mean_logits` at ~1e-4 due to torch/cuDNN kernel nondeterminism across GPU environments (frozen: torch 2.13.0+cu130; reproduced: torch 2.5.1+cu124). No reported metric is affected. Status in replay JSON: `MINOR_NUMERICAL_DRIFT`. All labels, accuracies, F1, confusion matrices, retrieval ranks, citations, and provenance are identical.

---

## Section: Authority Recovery (Base-30)

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| Recall@5 | 12/30 (0.40) | `e3_e4_reproduced_evaluation.json` → E3 recall_at_5 = 0.4 | VERIFIED_REPLAY |
| Recall@100 | 15/30 (0.50) | `e3_e4_reproduced_evaluation.json` → E3 recall_at_100 = 0.5 | VERIFIED_REPLAY |
| Absent at k=100 | 15/30 | Complement of Recall@100 | VERIFIED_REPLAY |
| Authority-consistency precision | 0.08 (12/150) | `e3_e4_reproduced_evaluation.json` → authority_consistent_precision = 0.08 | VERIFIED_REPLAY |
| Authority-consistency recall | 0.40 | `e3_e4_reproduced_evaluation.json` → authority_consistent_recall = 0.40 | VERIFIED_REPLAY |
| Authority-consistency F1 | 0.133 | `e3_e4_reproduced_evaluation.json` → authority_consistent_f1 = 0.133333 | VERIFIED_REPLAY |
| Structural ceiling | 0.20 (30/150, 5 shown, 1 credited) | Derived from 1/5 per case ceiling | VERIFIED_REPLAY |

---

## Section: Citation Integrity (Base-30, 150 citations)

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| Citation groundedness rate | 1.00 (150/150) | `e3_e4_reproduced_evaluation.json` → E3 citation_groundedness_rate = 1.0 | VERIFIED_REPLAY |
| Provenance validity rate | 1.00 (150/150) | `e3_e4_reproduced_evaluation.json` → E3 citation_provenance_validity = 1.0 | VERIFIED_REPLAY |
| Temporal violations | 0/150 | `e3_e4_reproduced_evaluation.json` → E3 temporal_violation_rate = 0.0 | VERIFIED_REPLAY |
| Unsupported claims | 0/30 cases | `e3_e4_reproduced_evaluation.json` → E3 unsupported_claim_rate = 0.0 | VERIFIED_REPLAY |
| Citation failure state (1)–(3) | 0 occurrences | Above replay evidence | VERIFIED_REPLAY |
| Citation failure state (4) (valid but non-matching) | 18/30 cases | Complement of Recall@5 (12 selected + missed cases) | VERIFIED_REPLAY |

---

## Section: BM25 Retrieval Equivalence

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| BM25 rebuild top-100 agreement | Ranking-level, 30 evaluated queries | `e3_e4_reproduced_evaluation.json` retrieval results | VERIFIED_REPLAY |
| BM25 is NOT byte-identical SQLite | Stated limitation (not a positive claim) | Documented in Limitations section | N/A |
| BM25 does not generalize beyond 30 queries | Stated limitation | Documented in Limitations section | N/A |

---

## Section: Cross-Corpus Identifier Alignment

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| Syntactic ILDC→eCourts candidates | 5,391 | Corpus construction audit | ARTIFACT_DERIVED |
| Content-aligned pairs (passed gate) | 11 / 5,391 | Corpus construction audit | ARTIFACT_DERIVED |
| Identifier-namespace collisions | 5,380 / 5,391 | Complement of above | ARTIFACT_DERIVED |
| Deduplication: deduplicated pairs | 8,927 | Corpus construction audit | ARTIFACT_DERIVED |
| Deduplication: accepted | 1,304 | Corpus construction audit | ARTIFACT_DERIVED |
| Deduplication: rejected | 7,623 | Corpus construction audit | ARTIFACT_DERIVED |

> [!NOTE]
> ARTIFACT_DERIVED means the number comes from the corpus construction log/audit, not from an independent re-execution in the validation replay. These numbers were established during pipeline construction and are not contested by any replay evidence.

---

## Section: Error Analysis (Frozen Read-Only)

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| E3/E4 evidence divergences | 0/30 | `e3_e4_reproduced_evaluation.json` | VERIFIED_REPLAY |
| Cases with correct retrieval + wrong prediction | 3 (2008_1629, 1981_187, 1982_29) | Frozen artifact read-only | ARTIFACT_DERIVED |
| Authority-recovery bucket: retrieved + selected | 12 | Recall@5 = 12/30 | VERIFIED_REPLAY |
| Authority-recovery bucket: retrieved + unselected | 3 (1980_133, 1981_55, 1985_40) | Frozen retrieval run | ARTIFACT_DERIVED |
| Authority-recovery bucket: absent at k=100 | 15 | Recall@100 complement | VERIFIED_REPLAY |

---

## Section: Corpus & Methodology

| Claim | Value | Evidence Source | Classification |
|-------|-------|----------------|----------------|
| eCourts PDF instances | 39,069 | Corpus manifest | ARTIFACT_DERIVED |
| Accepted PDFs | 39,066 | Corpus manifest | ARTIFACT_DERIVED |
| Total labelled chunks | 2,343,435 | Corpus manifest | ARTIFACT_DERIVED |
| Unique chunks in index | 2,036,981 | Corpus manifest | ARTIFACT_DERIVED |
| OCR-affected instances | Some (count not independently replayed) | Corpus audit | HISTORICAL |
| Post-OCR quality gate | Applied | Corpus construction log | ARTIFACT_DERIVED |
| Answer-key size | 30 cases | Replay confirmed 30/30 direct-content passes | VERIFIED_REPLAY |
| Probe development history (0/9→3/9→6/9→7/9) | Recorded from development records | Development log; not replayed | HISTORICAL |

---

## Removed/Excluded Claims (Scientific Freeze)

| Claim | Reason |
|-------|--------|
| Combined-37 outcome accuracy/F1 | Not independently replayed |
| Extension-7 retrieval results | Not independently replayed |
| 14-case LLM presentation comparison | Exploratory, non-independent |
| Exact OCR count (12 of 15 restored) | HISTORICAL — not independently replayed |
| 99.20% figure | Unverified provenance |
