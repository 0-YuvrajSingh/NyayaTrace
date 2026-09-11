# RQ3 final integration + integrity audit (exploratory LLM evaluation; no ratings collected here)

## Files inspected

Packet/protocol/selection/manifest: `rq3_evaluator_packet.md/.json`,
`rq3_evaluator_packet_manifest.json` (hidden mapping), `rq3_case_selection.json`,
`rq3_protocol.md`, `rq3_design_audit.md`, `rq3_packet_generation_report.md`.
Results (externally generated, copied in): `rq3_case_results.csv`,
`rq3_preferences.csv`, `rq3_results.json`, `rq3_report.md`.
Reference: `experiments/rq1/rq1_results.json` (evidence source; read-only).

## Counts

Evaluators: 4 (Gemini, Claude Sonnet 4.6, DeepSeek, GPT-5.6 Luna). Cases: 14
(frozen sample, exact match). Display observations: 112 (4×14×2). Forced
preferences: 56 (4×14). No duplicates in any key. Scores: all integers 1–5.

## Validation checks (all PASS)

14 cases per evaluator; both displays per case; all 5 dimensions per display;
112/56 counts exact; frozen ID set exact; no duplicate rows; hidden-mapping
application correct on all 112 rows (zero mismatches); every preference
agrees with the mapped condition (zero disagreements); aggregate means,
preference counts/rates, evaluator means, and case-level unanimity all
reproduced bit-exact from the CSVs.

## Independently recomputed metrics (match stored JSON exactly)

- evidence_linkage S 4.589286 / U 2.839286 / D +1.75 (56/56)
- citation_verifiability S 4.696429 / U 3.696429 / D +1.0
- traceability S 4.642857 / U 2.160714 / D +2.482143
- explanation_clarity S 4.732143 / U 2.214286 / D +2.517857
- transparency_inspectability S 4.642857 / U 2.660714 / D +1.982143
- overall S 4.660714 / U 2.714286 / D +1.946429
- preferences: structured 56/56 (100%), unstructured 0, tie 0; unanimous on
  all 14 cases; per-evaluator means match (Gemini 5.0/2.2, Claude 3.642857/
  3.057143, DeepSeek 5.0/2.8, GPT-5.6 Luna 5.0/2.8).

## Agreement: stored files agree

CSV → JSON → report markdown fully consistent (dimension table, evaluator
table, 56/56 counts, unanimity list). No discrepancy found; no fix applied.

## Duplicated evaluator output

DATA CHARACTERISTIC: DeepSeek and GPT-5.6 Luna rating vectors are byte-
identical across all 112 cells (already disclosed in results notes and
report §6; runs retained separately, not merged). No action taken per
instructions. Claude and Gemini patterns are distinct.

## Wording / overclaim check

Required disclaimers present: exploratory LLM-based (title, notes, §1/§5/§6),
NOT independent human evaluation, no human-rated effect claim, presentation
transparency only (never correctness). Absent: significance, human agreement,
human-subject evidence, correctness/retrieval/prediction improvement,
causality, production, generalization, p-values. The two flag-term hits
("human-subject", "legal correctness") are both negations. No overclaim.

## Frozen RQ1/RQ2 artifacts

Unmodified (hash-verified in integrity run below; RQ1/RQ2 files only read).
No frozen baseline file touched by this audit.

## Verdict: PASS — no files modified.
