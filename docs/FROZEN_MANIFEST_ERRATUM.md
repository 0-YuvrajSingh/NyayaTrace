# Frozen manifest erratum — documentation-only, no experiment change

This file reconciles stale hash references without modifying any frozen
experiment artifact. All experiment files below are byte-identical to their
Git HEAD blobs and unchanged since `v4-baseline-reproduced (2bd02b3)`.

## E1 results
- File: `artifacts/e1_baseline_results.json`
- Current/HEAD SHA-256: `70d51f6c95d0be90c3c0480bf59b81df62684dbb574b427004af8cbf239163f8`
- Freeze record (`config/reproducibility_freeze.json`): `0726043d7e2445886f7c8658e4c7b8560f321d079b3e8203aa2d5890c9ccf13d`
- Evidence: `git log -- artifacts/e1_baseline_results.json` = only `2bd02b3`;
  `git diff HEAD -- <file>` clean; `git show HEAD:<file>` hash matches worktree.
- Verdict: file is correct frozen artifact; freeze hash is stale documentation.
  Do not regenerate E1.

## E3/E4 evaluation
- File: `artifacts/e3_e4_evidence_augmented_evaluation.json`
- Current/HEAD SHA-256: `5414e00243073d00e2d1a1f7d1f886ce27491cbca363d7afb5cfcabd401332fd`
- Freeze record: `e28ea37e67e5d2b4a3d35e448bddba14b35573ed170f0726c394dc2aa0a16270`
- Evidence: same as E1; unchanged since `2bd02b3`, worktree matches HEAD.
- Verdict: file correct; freeze hash stale. Do not regenerate.

## Dataset manifest
- File: `corpus/dataset_manifest.md`
- Current/HEAD SHA-256: `795dd6ecfd959aa516d76f5e038ef3ae913b8b244b3e3111af253558c93e1560`
- Freeze record (`dataset_manifest.sha256`): `e57fa817b1ed351cfb98f7e10332e35429371388187276366b04126a15ae31f1`
- Evidence: `git log -- corpus/dataset_manifest.md` = only `2bd02b3`;
  worktree matches `HEAD:corpus/dataset_manifest.md` (restored from
  `corpus/corpus/dataset_manifest.md` with identical hash).
- Verdict: file correct; freeze reference stale.

## Runtime paths (restored, hashes verified)
- `corpus/ildc/single_train.parquet`: `0d878add7371ad0d9ed41f59b0753d6c45b5fb6ebaec78b2d6284fe2a884f4b3` MATCH freeze
- `corpus/ildc/single_validation.parquet`: `2140d52ecf8f9af5554c0ca9a8f15ca59994383d1e722298c1bb7ef419ca8fa1` MATCH
- `corpus/ildc/single_test.parquet`: `10cddb021db95645799c22a7db000234bde5f7657d54e5c8e2c70688b0a36efc` MATCH
- `corpus/ecourts/cleaning_record.json`: `6cf58140c663c6cf27a16276c20d570e2dde1a1d76a1ddf263aa929e3ea2076e` MATCH
- `corpus/dedup_matches.csv`: `b05d93d58935ac89163fffe8aadb560d23b8d4d6158eeffb0b46003436b274c0` MATCH
- `retrieval/bm25.sqlite` (copied from `retrieval/bm25-001.sqlite`):
  `3187f7fce824ea8ccc5a26d908936ce4b78e81238289ea69348cb861350d65fb` MATCH freeze + transfer manifest.
  Original `bm25-001.sqlite` preserved.

## Canonical layout established
- Scripts/configs expect `corpus/ildc/`, `corpus/ecourts/`, `retrieval/bm25.sqlite`.
- Only `corpus/corpus/ecourts/` had `cleaned/ + metadata/ + pdfs/ + acquisition_record.json + cleaning_record.json`
  with full 1950-2020 year coverage; deeper levels are partial (pdfs-only).
- Restored: `corpus/corpus/ildc -> corpus/ildc`,
  `corpus/corpus/ecourts -> corpus/ecourts`,
  `corpus/corpus/dedup_matches.csv -> corpus/dedup_matches.csv`.
- Leftover `corpus/corpus/corpus/...` retained untouched for review; 32 `(1).pdf`
  verified byte-identical on 2 samples, preserved (no deletion).

## Final release identity
- FINAL_RELEASE_COMMIT: `2f9b37c` (local HEAD, ahead of origin, not pushed)
- FINAL_MANUSCRIPT_SOURCE: `paper_master.tex`
- FINAL_PAPER_SHA256 (tex): `39f302010726a1038c7da54c45d0d111e706cdbefece65f67a0b652e27151d57`
- FINAL_PAPER_PDF_SHA256: `f06ed1df0d851dae02ca5e3951989192a319818236ef39d6e816dd86044ee01a`
- FINAL_EXPERIMENT_FREEZE: `config/reproducibility_freeze.json` (with above erratum)
- FINAL_BM25_SHA256: `3187f7fce824ea8ccc5a26d908936ce4b78e81238289ea69348cb861350d65fb`
- FINAL_CORPUS_MANIFEST: `corpus/dataset_manifest.md` (`795dd6ec...`)
