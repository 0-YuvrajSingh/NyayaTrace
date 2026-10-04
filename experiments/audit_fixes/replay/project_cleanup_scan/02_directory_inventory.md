# Directory inventory (from 01_full_inventory.csv; read-only scan)

| directory | files | bytes | inferred purpose |
| --- | --- | --- | --- |
| corpus/ | 39219 | 23807113242 | eCourts PDFs (39,088) + cleaned chunks + ILDC parquet + dedup; primary data, mostly ignored |
| experiments/ | 352 | 3526099989 | audit work: scripts, replay outputs, BM25 rebuild, E2 caches |
| retrieval/ | 1 | 2269376512 | frozen BM25 SQLite index (tracked? verify; 2.27GB single file) |
| artifacts/ | 176 | 1516375724 | frozen results, checkpoints, HF cache, figures, weeklies |
| validation_replay/ | 28 | 154188457 | second E2 cache copy (dup of replay e2_cache) + related |
| demo/ | 2477 | 93615068 | spring-api, ml-service, web (incl. node_modules JS/map/TS bulk) |
| submission/ | 25 | 1417779 | archive/final/figures + manifests + templates |
| figures/ | 5 | 71242 | paper figure PDFs (fig1-5) |
| scripts/ | 65 | 474308 | pipeline + loader scripts (tracked source) |
| src/ | 11 | 67122 | legal_xai package (tracked source) |
| tests/ | 11 | 31760 | pytest suite (tracked) |
| docs/ | 10 | 53954 | final audit reports (tracked) |
| config/ | 16 | 51720 | frozen configs (tracked) |
| answer_key/ | 15 | 305243 | authority key + extension (tracked) |
| scratch/ | 25 | 39724 | one-off JS audit scripts (tracked? verify) |
| validation_prep/ | 7 | 25335 | small prep files |
| docker/ | 2 | 562 | Dockerfiles |
| root | ~15 | ~600000 | paper variants, compose, manifests, README |

Note: top-level paper variants (master/revised/final/6page tex+pdf, docx) are root files, all untracked except master.
