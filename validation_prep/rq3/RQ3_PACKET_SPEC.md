# RQ3 independent human-evaluation packet spec (v3 — supersedes v2 for NEW reviews)

Status: SPEC + BLANK SCAFFOLD. Zero ratings recorded here. The Week 13
self-review (`artifacts/week13_review_response_completed.json`, 1 author,
`outside_reviewer: false`) is RETAINED as a fallback artifact and must never
be merged with independent ratings.

## 1. Design (evidence-constant A/B)

Same 7 fixed cases as v2 (`2008_1629`, `1980_105`, `1980_133`, `1981_55`,
`1985_40`, `1997_792`, `2013_35`) rendered from persisted, verified Week 11
E4 evidence sets. Structured vs unstructured displays differ ONLY in
presentation (citation-ID parity enforced by
`scripts/build_week13_rq3_review_packet.py` before any packet ships).
Reviewers are NOT asked to decide cases or assess legal correctness.

## 2. Blinding

- Reviewers see `Display 1` / `Display 2` only. Words "structured" /
  "unstructured" never appear in reviewer-facing material.
- The condition map (`case_id` → which display is structured) is sealed in a
  coordinator-only key file (`rq3_condition_key_<ROUND>.json`, never
  distributed) generated with the frozen per-case orders
  (`RANDOMIZATION_SEED = 20260903`) preserved for comparability.
- Reviewer identity is pseudonymized: enrolled IDs `R01`, `R02`, … Responses
  carry reviewer IDs only.

## 3. Randomization (pre-registered seeds, recorded in packet)

1. Per-case display order: frozen `presentation_orders()` (seed `20260903`).
2. Per-reviewer case sequence: `random.Random(20260903 + reviewer_index).shuffle`
   over the 7 cases; the shuffled sequence is printed on the reviewer's cover
   sheet and stored in their response file.
3. Coordinator records both seeds in the round log. No re-shuffling after
   distribution.

## 4. Instrument — six 1–5 Likert items per display (+ preference)

Scale for Q1–Q6: 1 = strongly disagree … 5 = strongly agree.

- Q1 `source_clarity`: "I can tell which authority each statement comes from."
- Q2 `source_finding_ease`: "I could locate the full source details quickly."
- Q3 `appropriate_trust`: "The display helps me place the right amount of trust
  without independently checking sources."
- Q4 `limits_clear`: "The display makes clear what the evidence does not show."
- Q5 `structure_navigation`: "The layout helps me inspect evidence efficiently."
- Q6 `overall_fitness`: "This display supports responsible legal research use."
- Free text: `notes` per display; then forced `comparison_preference`
  (`display_1` | `display_2` | `tie`) + `comparison_notes`.

## 5. Reviewer/case IDs + response recording

- Enrollment: coordinator assigns `R01…`, records background class
  (practitioner / academic / student / other) + date + `outside_reviewer: true`
  confirmation. Minimum target: 3 independent raters (enables Fleiss κ);
  5+ preferred.
- One response file per reviewer: `rq3_responses_<ROUND>_<REVIEWER>.json`
  conforming to `response_template_v3.json` (all ratings null until returned).
- Returned files are append-only: coordinator validates ranges (integers 1–5,
  preference enum) and logs receipt; never edits ratings.

## 6. Agreement + analysis (pre-registered; descriptive given N=7 cases)

- Primary: Fleiss κ per Likert item across raters (on structured-minus-
  unstructured difference direction AND on raw display scores), with
  percent agreement alongside (κ is unstable at small N — report both).
- Secondary: pairwise Cohen κ per item; exact (Clopper–Pearson) CI on the
  preference proportion; Wilcoxon signed-rank on paired structured vs
  unstructured means per item (descriptive, no confirmatory claim at N=7).
- Unit of analysis is the case (N=7, non-random): report case-level means,
  never pool ratings across cases as independent observations without a
  mixed-effects note. No legal-correctness inference from any statistic.

## 7. Build command (requires live provenance DB; NOT run in this prep phase)

`$env:LEGAL_XAI_DATABASE_URL = "<db-url>"` then
`python scripts/build_week13_rq3_review_packet.py` regenerates the v2 packet
artifacts; the v3 coordinator wrapper (seed handling, cover sheets, sealed
key, response files) is manual-per-round until a reviewer pool exists —
deliberately NOT automated further to avoid fabricating review logistics.
