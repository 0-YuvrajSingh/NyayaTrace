# RQ1 report — descriptive comparison on the frozen 37-case reference-evidence set

Question: does grounding in BM25-retrieved evidence improve legal-research
reliability / relevant-evidence retrieval vs the facts-only Legal-BERT
baseline? Design: E2 (facts-only, frozen checkpoint-6318, no evidence) vs E3
(same checkpoint/preprocessing/seed/corpus/index/top-k/temporal + retrieved
evidence). Read-time 37 assembly (30 frozen + 7 verified); both sources
byte-identical before/after (hashes in run manifest).

## Retrieval (primary)

| Set | R@5 | R@100 | Auth-P | Auth-R | Auth-F1 | Ground | Prov | TempViol | Unsupp |
|---|---|---|---|---|---|---|---|---|---|
| base30 (frozen, reproduced) | 0.40 (12/30) | 0.50 (15/30) | 0.08 (12/150) | 0.40 | 0.1333 | 1.0 | 1.0 | 0.0 | 0.0 |
| ext7 (new) | 0.00 (0/7) | 0.7143 (5/7) | 0.00 (0/35) | 0.00 | n/a (0/0) | 1.0 | 1.0 | 0.0 | 0.0 |
| combined37 | 0.3243 (12/37) | 0.5405 (20/37) | 0.0649 (12/185) | 0.3243 | 0.1081 | 1.0 | 1.0 | 0.0 | 0.0 |

The 7 added cases lower aggregate R@5 (12/30 → 12/37) and precision
(12/150 → 12/185) while raising R@100 (15/30 → 20/37): the extension
authorities are retrievable (5/7 at k=100, ranks 14–89) but none surfaces in
top-5 display. The frozen 30-case result is preserved unchanged alongside
(not replaced by) the 37-case evaluation.

## Prediction (secondary; does not answer RQ1 alone)

| Set | E2 acc / F1 | E3 acc / F1 |
|---|---|---|
| base30 | 0.7000 / 0.6534 [[5,2],[7,16]] | 0.6667 / 0.6032 [[4,3],[7,16]] |
| ext7 | 0.5714 / 0.5714 [[2,0],[3,2]] | 0.5714 / 0.5714 [[2,0],[3,2]] (identical) |
| combined37 | 0.6757 / 0.6442 [[7,2],[10,18]] | 0.6486 / 0.6073 [[6,3],[10,18]] |

Descriptive only (N=37/30/7 far below any significance threshold): on the
frozen 37-case reference-evidence set, adding retrieved evidence does not
raise outcome-prediction accuracy over the facts-only baseline, while
citation integrity remains perfect in both strata. No superiority claim is
made in either direction; no generalization, legal-correctness, or
completeness claim is made.

## Limits

Single-reporter reference (one expected authority/case); N=37 descriptive;
BM25-lexical selection bottleneck visible in both strata; distinguished
authorities (1991_87, 1991_136) absent at k=100. See rq1_error_analysis.md.
