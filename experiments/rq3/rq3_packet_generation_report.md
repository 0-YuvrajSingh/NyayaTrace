# RQ3 packet generation report (packet only; no ratings, no analysis)

- 14 cases generated, exact frozen IDs in fixed order: 2008_1629, 1980_105,
  1980_133, 1981_55, 1985_40, 1997_792, 2013_35, 1990_234, 1990_256,
  1990_324, 1991_136, 1991_87, 1992_286, 1993_90 (5 evidence items each).
- Parity: per-case evidence-ID sets Display1 == Display2 (asserted at build;
  base7 cross-checked against frozen parity audit orders; ext7 renders
  parity-checked in code). All 14 parity_pass = true. STOP never triggered.
- Base7: verbatim bodies from frozen `week13_review_packet.md` (condition
  headers stripped, content untouched). Ext7: deterministic renders from
  RQ1-identical selected evidence (source_ids asserted equal to
  `rq1_results.json`) + corpus verbatim via frozen render functions.
- Blinding: seed 20260903 orders from `rq3_case_selection.json` (base7
  replicates frozen orders — verified); mapping ONLY in hidden manifest.
- Leak review: no condition/expected-authority/rank/prediction metadata in
  evaluator files. Residual matches reviewed benign: "E4" = evidence-ID
  labels (E1–E5) inside content; "control/Controller" = judgment text
  (e.g. rent Control Order); one "experimental" in draft instructions
  reworded to neutral and re-verified absent. No hidden manifest embedded.
- Source hashes recorded in hidden manifest (11 inputs).
- No ratings collected (`rq3_evaluation_data.csv` 0 rows); no RQ3 analysis;
  no self/LLM evaluation; no frozen artifact modified.
- Determinism: base7 byte-derived from frozen packet; ext7 re-derivable via
  logged retrieval parameters (frozen configs); builder scripts retained in
  temp (not repo) — rerun reproduces identical selection (asserted
  RQ1-identical at build time).
