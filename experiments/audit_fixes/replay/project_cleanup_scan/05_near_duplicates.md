# Near duplicates (byte-differing variants)

## Paper manuscripts (similarity = difflib ratio on .tex)
| pair | similarity | what changed |
| --- | --- | --- |
| paper_master_final.tex vs paper_master_6page.tex | 0.72 | distinct variants (final 813 lines/6pp/4516w vs 6page 781 lines/6pp/3720w); different compression lineages — see paper audit 06 |
| paper_master.tex vs revised/final | high (unmeasured) | 11 factual corrections + compression passes (see revision_change_log.md) |
| paper_master_original_backup.tex (replay/) | exact dup of paper_master.tex expected | backup, see 04 |

Binaries compared by size+SHA only: paper_master.pdf (293,984) vs revised (294,801) vs
final (204,518/205,133?) vs 6page (222,823) — all distinct builds. Do NOT infer equivalence.

## Audit scripts (name-similar, content differs — verified by size/content reads)
- bm25_deep_compare.py (5,216) vs bm25_deep_compare2.py (4,545): v2 supersedes v1
  (indexed-temporal rewrite). Keep v2 tooling; v1 REVIEW.
- bm25_deep_compare_runner.sh vs runner2.sh; run_e2_repeat.sh vs run_e2_repeat2.sh;
  generate_manifest.py vs generate_manifest2.py; c6_check.py vs c6_check2.py:
  versioned pairs, newer supersedes. See 07 for keep recommendations.
- rebuild_final_batch*.py (13 files) vs sixpage_batch*.py (7 files): per-pass rebuild
  scripts for final and 6page lineages; history, not active tooling. See 07.
- e1_test1.json vs e1_test2.json vs e1_test.json: differ only in model_artifact path
  field (canonical IDENTICAL per audit). Keep as determinism evidence.
- e2_test_predictions.json vs e2_test_predictions_repeat.json: identical bytes
  (exact dup, see 04).
- ecourts_corpus_identity.json (artifacts vs replay copies): exact dup (see 04).
- .aux/.log/.out triplets per paper variant (revised/final/6page): build byproducts,
  regenerable via pdflatex. See generated list.
- e1_model.joblib vs e1_model1/2.joblib vs e1_reconstructed_model.joblib: same size
  class (~2.08MB), distinct hashes — separate refits, keep as evidence.
- bm25.sqlite (retrieval, 2,269,376,512) vs replay/bm25.sqlite (same size, SHA differs:
  3187F7… vs F2A70B…): rebuilt index, logically equivalent, bytes differ. NOT duplicates.
- audit_fixes_manifest.json vs replay copy: compare before action (see 08).
