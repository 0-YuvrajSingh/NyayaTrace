# Final verification matrix + decision lists (do not edit the manuscript)

| Area | Status | Critical issues |
| Quantitative claims | PASS WITH CAVEAT | combined-37/extension/LLM numbers artifact-only; 1985_40 wording; 29-count precision |
| Population definitions | PASS WITH CAVEAT | issue 1 (1985_40 selected wording) |
| Metric definitions | PASS | none; rounding consistent |
| E1 | PASS | C-search consumed, refit recomputed |
| E2 | PASS | training consumed, inference exact x2 |
| E3/E4 | PASS WITH CAVEAT | fp16 logit noise; strict-hash mismatch explained |
| BM25 | PASS WITH CAVEAT | ranking-level only; raw SQLite SHA differs |
| Leakage | PASS WITH CAVEAT | top-5 scope only |
| Answer-key audit | PASS | mapping re-derivation not re-run |
| Legal citations | REVIEW REQUIRED | Pooja Singh external sourcing + URL conflict |
| References | REVIEW REQUIRED | taxflow2026 authors; URL; minor formatting |
| Limitations | PASS WITH CAVEAT | add fp16 sentence; TS-compile evidence |
| Originality | PASS | generic/expected overlaps only |
| Abstract/conclusion | PASS | numbers trace; qualifiers retained |

## A. SAFE TO STATE
- 1517 → 14 excluded → 1503 evaluated populations and all E1/E2 metrics, class F1, confusion matrices.
- E2 inference exact reproduction (×2, bit-identical records, file hash match).
- E1 deterministic refit canonical IDENTICAL.
- Base-30 Recall@5 12/30, Recall@100 15/30, provenance/groundedness 1.0, 0 violations, authority precision 0.08 (ceiling 0.20), from recomputed runs.
- E3/E4 decisions, evidence IDs, flags, metrics identical between frozen and recomputed runs.
- BM25 same corpus/IDs/params with 30/30 top-100 ranking agreement on evaluated queries.
- 0/30 self in top-5; 0 temporal violations in top-5.
- 81 pytest / 6 FastAPI / 8 Spring tests passing.
- Checkpoint-6318 SHA 924a5bb9…dbdc773.
- Alignment counts 5391→11 and 8927/1304/7623 as cited-artifact findings.
- Error-overlap table values 684/238/213/368 and 18/3/3/6 (join arithmetic verified).
- All abstract/conclusion numbers that appear in body tables above.

## B. MUST REWORD
- 1985_40 "retrieved and selected" → retrieved-only for that case.
- "29 byte-exact" → 28 + 1 line-ending-normalized + 10 metadata-differing.
- "guarantee no post-dating" → scoped to metadata + fail-closed assumptions.
- Any E3/E4 "exact reproduction" phrasing → "identical decisions/metrics with bounded fp16 logit variation."
- Any BM25 identity phrasing → "ranking-level equivalence on the evaluated query set."
- Leakage → state exact scope (top-5), never "no leakage whatsoever."

## C. MUST NOT STATE
- Combined-37 / Extension-7 / LLM-rater numbers as independently replayed.
- Positive controls, probe steps, OCR counts, 99.20% figure as replay-verified (artifact-supported only).
- TypeScript compile as evidenced (no log cited).
- Pooja Singh holding as repo-verified (externally sourced).
- Byte-identical BM25 or E3/E4 payloads.
- Universal ranking equivalence beyond evaluated queries.
- Human preference or legal correctness from the LLM presentation comparison.
