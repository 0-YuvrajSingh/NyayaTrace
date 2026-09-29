# 02 — Credential Dependency Audit

Comprehensive repository search for consumers of `experiments/audit_fixes/replay/.db_env` and the `LEGAL_XAI_DATABASE_URL` environment variable.

---

## 1. Directory-by-Directory Audit

| Directory / Subsystem | Direct Reference to `.db_env` | Consumer Classification | Notes |
|:---|:---|:---|:---|
| **`scripts/`** | None | `NO_REFERENCE` | Scripts use `os.getenv("LEGAL_XAI_DATABASE_URL", DEFAULT_DATABASE_URL)`. |
| **`src/`** | None | `NO_REFERENCE` | Zero file or path references to `.db_env`. Accepts `database_url` as parameter. |
| **`config/`** | None | `NO_REFERENCE` | `reproducibility_freeze.json` documents that credentials are deliberately excluded from freeze. |
| **`compose.yaml`** | None | `NO_REFERENCE` | Uses `${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}`. No `env_file` declaration. |
| **`compose.demo.yaml`** | None | `NO_REFERENCE` | Uses `${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in the environment}`. No `env_file`. |
| **`docker/`** | None | `NO_REFERENCE` | `docker/e2.Dockerfile` sets standard Python paths and HF cache dirs; no `.db_env`. |
| **`demo/`** | None | `NO_REFERENCE` | `demo/ml-service/app.py` reads `DATABASE_URL_ENV = "LEGAL_XAI_DATABASE_URL"`. |
| **`tests/`** | None | `NO_REFERENCE` | No test references `.db_env`. |
| **`experiments/audit_fixes/scripts/`** | Yes | `AUDIT_REPLAY` | `rotate_db_password.py` rotates password; replay scripts run via `docker --env-file`. |
| **`experiments/audit_fixes/replay/`** | Yes (logs/notes) | `HISTORICAL` | `AUDIT_GAPS_UPDATE.md` and cleanup scan manifests record rotation and replay history. |
| **`.gitignore`** | Yes (line 48) | `DEVELOPMENT_ONLY` | Safety exclusion preventing Git tracking. |

---

## 2. Ingestion Mechanism Analysis

1. **Docker Compose `env_file`:**
   - Neither `compose.yaml` nor `compose.demo.yaml` loads `.db_env`.
2. **Dotenv / Automatic Loaders:**
   - No `python-dotenv` or automatic `.env` loader is invoked by `scripts/` or `src/` to search for `.db_env`.
3. **Command-Line Invocations:**
   - `.db_env` was exclusively supplied via explicit CLI flag: `docker run --env-file experiments/audit_fixes/replay/.db_env ...` during the Phase 16 audit replay.
4. **Active Runtime Consumers:**
   - **Zero** active runtime services depend on `.db_env`.
