# Final scope-alignment report — paper consistency pass (text-only, identifiers + wording)

Source of truth: canonical `Indian_Legal_XAI.docx` (Document 3 Final).
Edited source: `submission/paper.md` ONLY (Markdown source of the paper).
No code, data, key, result, config, or experiment file touched. No numbers
recomputed or restyled. No commit/push.

## 1. Terminology corrections made (`submission/paper.md`)

1. §5 RQ list replaced (4 items → exactly 3 canonical RQs, verbatim scope
   wording for RQ1/RQ2/RQ3) plus explicit mapping sentences: E2-vs-E3 is
   the RQ1 controlled grounding comparison; E1 is contextual traditional
   baseline only.
2. RQ4 designation removed (1 occurrence found: §5 bullet; now 0).
   Underlying prediction content retained and relabeled as secondary
   prediction analysis under RQ1/RQ2 (adjusted the §5 closing paragraph;
   §9.2 already framed it as descriptive revision content).
3. §11.2: added one sentence barring the E1-vs-E2 misreading (E1
   contextual; RQ1 answered via E2-vs-E3 retrieval + subset analyses).
4. §13.8: added blinded-LLM-exploratory sentence (self-review remains
   labeled non-independent; LLM comparison explicitly not human evidence).
5. §13.9: added static-demo (not React/Spring), unreported
   latency/memory/compute, and no-standalone-diagram sentences.

## 2. RQ4 occurrences

Found: 1 (`§5` list bullet). Removed: 1. Remaining: 0 (verified by scan).

## 3. RQ1 labeling corrections

- §5 bullet rewritten to canonical grounding question (was "Outcome
  baselines" E1-vs-E2 comparison).
- Added E2-vs-E3-as-RQ1 mapping in §5 and §11.2. E1 kept strictly as
  traditional baseline context wherever reported.

## 4. 30-case vs 37-case wording

Paper contains no "37" reference at all (verified): nothing to correct and
nothing implied about preregistration. The 30-case frozen results are
quoted unchanged. The additive 37-case analyses live outside the paper in
`answer_key/extension_v6/` + `experiments/rq1/` with their own
non-preregistration disclosures; if the paper later cites them, the
additive/post-freeze framing must accompany the numbers.

## 5. Temporal wording

Already conformant (strictly-earlier-year rule + year-only ILDC
constraint + same-year ambiguous exclusion + no day-level claims + novelty
kept bounded). No edit required; verified, not assumed.

## 6. Limitations added/confirmed

Confirmed present: ILDC/Supreme-Court scope, statute-version scope,
OCR/facts approximation, answer-key size/era, single-authority coverage,
recovery gap, year granularity, bundled verification, self-review +
uncalibrated uncertainty, semester scale, governance. Added: LLM
exploratory status, demo-stack form, efficiency-metrics absence,
diagram-file absence.

## 7. Forbidden-claim scan

No human-evaluation-for-RQ3 claim; no significance claim (sole
"significance" hit is future-work McNemar context); no autonomy,
multilingual-core, GraphRAG/agents, SaaS, or prediction-as-sole-objective
claims ("proves" hit is a negation). No edit required.

## 8. Files modified

- `submission/paper.md` (5 small text edits above; numbers/style untouched).
- `docs/FINAL_SCOPE_ALIGNMENT_REPORT.md` (this file; new).

## 9. Known staleness (not repaired — no toolchain in repo)

`submission/paper.html` and `submission/paper.pdf` were generated from the
pre-edit Markdown (README confirms md→pdf lineage) and now lag the source
by these wording-only edits. No pandoc/wkhtmltopdf available locally, and
regenerating the PDF outside the original toolchain risks formatting
divergence, so regeneration is deferred to submission time and recorded
here rather than improvised.

## 10. Verification

Tests + git scope reported in the closing check. Result artifacts,
datasets, keys, configs, and implementation hashes untouched (paper.md is
documentation, not an experiment artifact; no result value altered).
