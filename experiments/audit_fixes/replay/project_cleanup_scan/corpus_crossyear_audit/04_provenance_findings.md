# Provenance findings (read-only)
- Year folders (`corpus/ecourts/pdfs/year=YYYY`, `metadata/year=`, `cleaned/year=`)
  mirror the SOURCE ARCHIVE partition (S3 per-year tarballs; acquisition_record.json
  per-year source counts). Folder year = source-partition year, NOT verified decision year.
- 5,177/5,181 clean pairs share filenames; 5,134 have gap 1 (consecutive years),
  concentrated 1961–1976: the source lists the same PDF under two adjacent year
  partitions (SCR-volume-year vs decision-year dual listing — consistent with the
  known year skew, not independently proven per file).
- 4 pairs span gap 0 (same folder, different names) and one 4-file group holds TWO
  filenames (1980_2_292_297 vs 1980_2_293_297) with identical bytes in both
  year=1979/1980: possible source-side mislabeling → duplicate chunk sets may exist
  under two source_ids. Corpus-quality question for the owner; NOT a deletion matter.
- Indexed corpus resolves each pair to ONE logical source: cleaned chunk records carry
  no folder path (path/source_id = filename stem; audit dict keeps one side per stem);
  DB source_path is a bare ID (e.g. 1982_2_365_1455, 4,306 chunks). Runtime
  (retrieval/eval/training) never touches year folders.
- Build/audit provenance DOES touch them: per-year acquisition counts (39,069 total),
  audit availability counts, cleaned outputs per year. Deleting sides alters corpus
  construction reproducibility and count traceability.
- Nested-cleanup distinction: 0/5,182 paths carry nested markers ((1)/corpus/corpus);
  0/5,182 SHAs occur in the 3,529-record nested manifest. Separate phenomena confirmed.
