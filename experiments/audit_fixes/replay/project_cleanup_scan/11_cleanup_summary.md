# Cleanup summary (scan only — nothing deleted, moved, or renamed)

- Files scanned: 42,469 (31,370,667,970 bytes); tracked 459; ignored 41,708
- Directories: top-level 19 + recursive (see 02)
- Exact duplicate groups: 5,320 (5,182 = cross-year corpus PDF pairs)
- Near-duplicate groups: ~15 (paper variants, script version pairs, JSON refits)
- Generated files: ~2,900 (node_modules, target/, tex build outputs, pass logs, HF placeholders)
- Temporary/stray candidates: ~40 scripts + ~60 build logs; zero classic stray patterns
- Suspicious/broken: 3 (BOM manifest LOW; 0-byte docker_info LOW; 6page provenance REVIEW)
- Secret findings: 1 live credential file (HIGH, protected) + rotated-history note (MEDIUM)
- Large-file candidates: top-50 in _large.json (indexes, checkpoints, caches, corpus PDFs)
- Redundant-appearing scripts: ~20 (version pairs + rebuild history + stat counters)
- Paper revisions: master (tracked) + revised + final + 6page + docx + submission/final
- Replay artifacts: ~40 evidence/report/output files
- Recommended DELETE_LATER: 7 groups; REVIEW_MANUALLY: 6; rest KEEP/ARCHIVE/CONSOLIDATE

## DEFINITELY KEEP
src/, scripts/ (minus superseded review), tests/, config/, answer_key/, figures/,
demo sources, paper_master.tex/.pdf, frozen artifacts + checkpoint,
replay evidence outputs + final audit reports, .gitignore as-is.

## LIKELY SAFE TO DELETE LATER
replay/e2_hf_cache/ (post-replay), replay/spring-api-copy/, tex pass logs + aux/log/out,
0-byte docker_info.log, demo build outputs (node_modules, target/), superseded probe scripts.

## DO NOT DELETE YET
corpus year-folder pairs, validation_replay/, artifacts/figures/, 6page variant,
original backups, .db_env, rebuild-batch history, BOM manifest, anything referenced
by code/docs/paper or with reproducibility value.
