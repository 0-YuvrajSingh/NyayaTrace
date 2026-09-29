# Paper issue list (do not edit the manuscript)

1. [accuracy] Error Analysis lists 1985_40 among cases that "retrieved and selected" yet predicted wrong; frozen flags show retrieved=True, selected=False (rank 78). Fix wording to three selected + one retrieved-only. (paper L854–857)
2. [precision] Reproducibility says "29 byte-exact" freeze entries; week16 records 28 byte-exact + 1 CRLF-normalized + 10 differing. Qualify the count. (paper L1035–1037)
3. [wording] "guarantee that no displayed authority can post-date the matter" is unconditional; scope to metadata + fail-closed assumptions. (paper L218)
4. [wording] E3/E4 must not be described as byte-identical payloads; supported phrasing is "identical confusion matrices / decisions / metrics with fp16 logit noise only." No offending sentence found; keep on reword watch.
5. [wording] BM25 equivalence must stay at "same corpus/IDs/params + 30/30 ranking agreement on evaluated queries"; no byte-identity sentence exists — do not add one.
6. [scope] Leakage evidence covers top-5 + temporal + dedup; do not claim "no data leakage whatsoever."
7. [citation] taxflow2026 author initials incomplete. (References)
8. [citation] "et al." inconsistency (legalbench2023, lewis2020); legalbench2023 missing pages. (References)
9. [citation] poojasingh2026 order-copy URL host + one-char hash conflict with archive copy; confirm correct link externally. (References)
10. [latex] `\texttt\{YYYY\_N\}` renders braces outside monospace; use `\texttt{YYYY\_N}`. (L125)
11. [evidence] 1985_40 displayed-passage topic gloss not cross-checked. Either verify or soften to illustration-only (already labeled illustration; keep).
12. [evidence] Positive controls 37/37×3, probe pathway 0/9→7/9, OCR 12/3, 99.20% truncation figure, extension ranks 14/16/26/32/89: artifact-only, no independent replay — do not upgrade their status beyond cited-artifact support.
13. [evidence] Combined-37 and Extension-7 numbers: artifact-only (base-30 replayed). Keep strata language; do not present combined as independently replayed.
14. [evidence] LLM RQ3 (56/56, deltas, means) and self-review means: NOT VERIFIED by replay; presentation-only qualifier must be retained everywhere.
15. [evidence] TypeScript compile claim in Reproducibility lacks a cited log; attach or drop.
16. [limitations] Add one sentence naming GPU fp16 logit non-determinism (bounded, decision-preserving) to Limitations.
17. [external] Pooja Singh 2026 holding depends on external legal sourcing; repo holds no verification artifact.
18. [training] E2 training hyperparameters and E1 C-search were consumed from frozen records, not re-executed; inference/refit were recomputed. Keep method text from implying retraining.
