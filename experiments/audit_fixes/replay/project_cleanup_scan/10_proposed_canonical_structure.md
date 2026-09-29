# Proposed canonical structure (based on actual contents; no changes made)

```text
src/                 # legal_xai package (canonical source)
scripts/             # pipeline + loader scripts (canonical source)
config/              # frozen configs (canonical)
tests/               # pytest suite (canonical)
corpus/              # data only: ecourts PDFs, cleaned chunks, ildc parquet, dedup
retrieval/           # frozen bm25.sqlite (reproducibility artifact)
artifacts/           # frozen results, checkpoints, HF cache, figures, weeklies
answer_key/          # authority key + extension (canonical evaluation ref)
demo/                # spring-api, ml-service, web (demo stack; build outputs ignored)
docker/              # Dockerfiles
docs/                # final audit reports
experiments/         # audit work (NOT canonical source): audit_fixes/{scripts,replay}
figures/             # paper figure sources (canonical for manuscript)
submission/          # submission packaging + archive + manifests
scratch/             # one-off analysis scripts (non-canonical, keep-or-archive)
validation_prep/ validation_replay/  # small/legacy replay dirs (role unclear -> REVIEW)
paper_master*.tex    # manuscript lineage at root (needs canonical-selection decision)
```

Notes: `experiments/` and `scratch/` are work areas, not canonical source. Duplicate
caches (e2_hf_cache ×2, e2_cache ×2 incl. validation_replay) and copied trees
(spring-api-copy) live outside canonical paths and are the main consolidation targets.
