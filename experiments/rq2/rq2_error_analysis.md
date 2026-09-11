# RQ2 error analysis (observed categories only)

Live-data outcome (37/37): category 8 — no difference between E3 and E4
outputs. All 185 displayed citations pass verification (150 base + 35 ext);
0 temporal violations, 0 unsupported answers, 0 items rejected by D that A
accepted. No failures were discarded; there was nothing to discard.

Positive-control probes (same unchanged verifier, mutated inputs):
- altered verbatim passage → rejected 37/37 (passage-mismatch fires);
- fabricated authority citation → rejected 37/37 (authority-metadata
  mismatch fires);
- backdated query year (authority_year − 1) → rejected 37/37
  (temporal-ineligibility fires).

Observed taxonomy mapping: categories 1 (valid evidence retained) applies
to all 185 items; categories 2–7 are attested ONLY by the probes (the gate
mechanisms demonstrably bite), not by live-data failures. No failure was
invented to fill the taxonomy.
