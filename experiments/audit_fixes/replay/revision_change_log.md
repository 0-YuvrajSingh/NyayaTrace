# Revision change log (paper_master.tex → paper_master_revised.tex)

Original preserved at `experiments/audit_fixes/replay/paper_master_original_backup.tex`
(SHA-256 9DE053A7C74F8807D86100C5D2FB9C93DDB602EFC140EE59B, identical to the pre-edit original).
No validated experimental value was changed. No new numbers, citations, or results added.

| Location | Original issue | Revision | Evidence |
| -------- | -------------- | -------- | -------- |
| Abstract (Pooja Singh) | Ruling stated as fact without repo verification | Attributed to "the order copy cited here" | paper_citation_audit.md (NOT VERIFIED, URL conflict) |
| Introduction L92–96 (Pooja Singh) | Same as above | "According to the order copy cited here, in …" | same as above |
| Introduction identifier example | Malformed `\texttt\{YYYY\_N\}` | `\texttt{YYYY\_N}` | citation audit L5 (low) |
| Problem Formulation (temporal) | Unconditional "guarantee" | Scoped to fail-closed metadata checks | issue list 3; leakage/temporal audit (0 violations observed, conditional) |
| Error Analysis (4 cases) | 1985_40 listed as "retrieved and selected" | Three selected + 1985_40 retrieved-but-not-selected | frozen flags (retrieved=True, selected=False, rank 78); issue list 1 |
| Results (positive controls) | "Three positive controls" read as fresh proof | "Three recorded positive controls" | issue list 12 (artifact-only) |
| Limitations (new) | No fp16 disclosure | Added Inference-numerics paragraph (bounded 4th-decimal variation, no decision change) | E3/E4 diff (max 7.7e-4); issue list 16 |
| Limitations (new) | No BM25 scope statement | Added ranking-level-scope paragraph (30 evaluated queries; not byte-identical; no generalization) | bm25_deep_compare.json 30/30; issue list 5 |
| Limitations (era paragraph) | 14-case filter not framed | Added narrowing sentence | e1/e2 splits (1517→14→1503) |
| Reproducibility (freeze) | "29 byte-exact" | "28 byte-exact, one line-ending-normalized, and 10 differing" | week16 RR-01/RR-02 |
| Reproducibility (demo) | Unevidenced TypeScript-compile claim | Clause removed; Spring 8/8 + FastAPI 6/6 retained | issue list 15; spring_retest.log, fastapi log |

Deliberately unchanged (STOP condition — would require inventing evidence):
taxflow2026 author names; "et al."/missing-page formatting; poojasingh2026 URL selection;
combined-37/extension/LLM numbers (kept with existing strata/exploratory qualifiers);
probe/OCR/99.2% figures (kept as process records, now explicitly "recorded" where reproduced-claim risk existed).
