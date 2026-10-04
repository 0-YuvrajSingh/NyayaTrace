# 00 — Pre-Cleanup Baseline Snapshot

Pre-mutation repository baseline captured before executing any deletion operations for Prompt 19.

---

## 1. Global Repository Metrics

- **Total Non-Git Files:** 40,004
- **Total Non-Git Directories:** 327
- **Total Non-Git Volume:** 31,287,505,034 bytes (29.139 GB)
- **Git Tracked Files:** 459 files
- **Git Untracked Entries:** 9 entries
- **Git Ignored Root Entries:** 20 entries

---

## 2. Top-Level Directory Sizes (Excluding `.git`)

| Directory / File Category | Files | Total Bytes | Size (MB / GB) |
|:---|---:|---:|---:|
| `corpus/` | 39,219 | 23,807,113,242 | 22.70 GB |
| `experiments/` | 321 | 3,536,255,750 | 3.37 GB |
| `retrieval/` | 1 | 2,269,376,512 | 2.16 GB |
| `artifacts/` | 176 | 1,516,375,724 | 1.45 GB |
| `validation_replay/` | 28 | 154,188,457 | 147.05 MB |
| `submission/` | 25 | 1,417,779 | 1.35 MB |
| `scripts/` | 65 | 474,308 | 0.45 MB |
| `answer_key/` | 15 | 305,243 | 0.29 MB |
| `demo/` | 43 | 296,371 | 0.28 MB |
| `figures/` | 5 | 71,242 | 0.07 MB |
| `src/` | 11 | 67,122 | 0.06 MB |
| `docs/` | 10 | 53,954 | 0.05 MB |
| `config/` | 16 | 51,720 | 0.05 MB |
| `scratch/` | 25 | 39,724 | 0.04 MB |
| `tests/` | 11 | 31,760 | 0.03 MB |
| `validation_prep/` | 7 | 25,335 | 0.02 MB |
| `docker/` | 2 | 562 | < 1 KB |
| `.vscode/` | 1 | 40 | < 1 KB |
| Root files (manuscripts, configs, etc.) | 23 | 1,380,950 | 1.32 MB |

---

## 3. File Type Extension Breakdown (Top 20)

| Extension | Count |
|:---|---:|
| `.pdf` | 39,089 |
| `.json` | 179 |
| `.md` | 173 |
| `.py` | 173 |
| `.parquet` | 74 |
| `.jsonl` | 71 |
| `.log` | 41 |
| `.npy` | 30 |
| `.js` | 25 |
| `.csv` | 21 |
| `.sh` | 16 |
| `[no extension]` | 15 |
| `.lock` | 12 |
| `.txt` | 11 |
| `.java` | 11 |
| `.svg` | 10 |
| `.tex` | 6 |
| `.joblib` | 5 |
| `.mjs` | 4 |
| `.html` | 4 |

---

## 4. Current Git Status

```text
 M .gitignore
?? experiments/audit_fixes/
?? paper_master_6page.pdf
?? paper_master_6page.tex
?? paper_master_final.pdf
?? paper_master_final.tex
?? paper_master_revised.pdf
?? paper_master_revised.tex
?? scripts/timed_e2_repeat.py
```

---

## 5. Frozen Scientific & Manuscript Baselines (SHA-256)

| Artifact | Byte Size | SHA-256 Digest |
|:---|---:|:---|
| `paper_master_final.tex` | 37,222 | `FADC2392166664C60FB18365557BF065123AD62DE476F81A94DA3FAC236F961C` |
| `paper_master_final.pdf` | 204,518 | `93EECD93CBD2EA8D98266703E93D020B656C986858C282DC3326193F75EDB712` |
| `paper_master.tex` | 55,994 | `9DE053A7C74F8807D86100C5D2FB9C93DDB602EFC140EE59B9808903D0F06D2A` |
| `paper_master.pdf` | 293,984 | `3B35C27966D72EE7DABECBA6329A771E71ADBBBCA03E3DCAF1D721E97763EBBD` |
| `retrieval/bm25.sqlite` | 2,269,376,512 | `3187F7FCE824EA8CCC5A26D908936CE4B78E81238289EA69348CB861350D65FB` |
| `artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/model.safetensors` | 437,958,648 | `924A5BB9078BCC212EF07ACB9F08DFAA8593E880AE3868203DEB28586DBDC773` |

---

## 6. Corpus & Dataset Baseline Counts

- **Corpus PDF Count (`corpus/ecourts/pdfs/**/*.pdf`):** 39,068 files
- **Corpus Metadata Parquet Count (`corpus/**/*.parquet`):** 74 files (71 yearly partitions in `ecourts/metadata/` + 3 ILDC splits)
- **Corpus Cleaned JSONL Count (`corpus/ecourts/cleaned/**/*.jsonl`):** 71 files
- **Authority Answer Key (`answer_key/authority_answer_key.json`):** 30 verified cases
