# Source / config duplication + security map (scan only)

## 09 — source duplication
- `experiments/audit_fixes/replay/spring-api-copy/`: full copy of `demo/spring-api/`
  incl. `src/` + `target/` (jar byte-identical, see 04). No other source trees copied
  into experiments/ or replay/ found. src/, scripts/, tests/ have no internal dupes
  observed (11/65/11 files, distinct names).
- `demo/web` node_modules (1,430 JS + 412 map + 217 TS): dependency bundle, ignored.
- docker contexts: `docker/` (2 files) + Dockerfiles inside demo subdirs? verify — no
  copied-context duplication detected beyond spring-api-copy.
- scripts/timed_e2_repeat.py (untracked, root scripts/): audit helper, keep with audit.

## 12 — config duplication
- Canonical: config/*.json (16 files, tracked) — frozen E1/E2/E3-E4/evidence/facts configs.
- `demo/spring-api/pom.xml` canonical for demo; no competing Maven config found.
- `requirements.txt` (76B root) vs demo requirements? check demo/ml-service for pins.
- compose.yaml vs compose.demo.yaml: environment-specific pair (not dupes).
- `.db_env` (replay, ignored): ONLY live credential file. No `.env` files anywhere.
- No TOML found at top level (verify via inventory ext list).

## Secrets found (values NEVER printed)
| file | type | tracked? | ignored? | severity | action required |
| --- | --- | --- | --- | --- | --- |
| experiments/audit_fixes/replay/.db_env | live DB URL + password | no | yes | HIGH | ROTATE again before any sharing; keep protected while replays may run |
| compose.yaml:8 | password variable reference (no literal) | yes | no | LOW | none (interpolation only) |
| compose.demo.yaml | password variable refs + commented example | yes | no | LOW | none |
| scripts/.../rotate_db_password.py:19 | reads password from file (no literal) | no | no | LOW | none |
| Git history | prior session commands may contain old (rotated) password | n/a | n/a | MEDIUM | old password already rotated+rejected (verified); do NOT rewrite history |
| replay/logs/*.log | scanned clean (no secret patterns matched) | no | no | none | none |
| audit .md reports | scanned clean | no | no | none | none |

## 13 — large files (top by size; full top-50 in _large.json)
1. replay/bm25.sqlite 2,269,376,512 (rebuilt index — evidence)
2. retrieval/bm25.sqlite 2,269,376,512 (frozen index)
3. corpus PDFs up to ~69MB each (39,088 files, 23.8GB; 5,182 exact cross-year dup groups)
4. HF blobs 534MB ×2 ×2 locations (e2_hf_cache dup)
5. e2_cache npy 69MB/19MB ×2 locations (replay vs validation_replay)
6. checkpoint model.safetensors 437,958,648 (artifacts, frozen)
7. spring jars 21MB ×2; e3e4_replay.json 1.4MB; joblibs ~2MB ×4

## 14 — broken / suspicious
| path | problem | severity | action |
| --- | --- | --- | --- |
| artifacts/local_cleanup/corpus_consolidation_manifest.json | malformed JSON (UTF-8 BOM; parses with utf-8-sig) | LOW | normalize encoding later |
| replay/logs/docker_info.log | 0 bytes (capture failed) | LOW | recapture or drop later |
| 20 HF `.lock`/`.no_exist` empties | normal HF cache placeholders | none | ignore |
| replay/bm25_ranking_probe.json (117B) | vacuous 0-query result (superseded) | LOW | archive later |
| paper_master_6page lineage | unknown authorship/provenance | REVIEW | owner decision |
