# 03 — Runtime Configuration & Necessity Evaluation

Evaluation of whether the PostgreSQL/Docker environment requires `experiments/audit_fixes/replay/.db_env`.

---

## 1. Active Configuration Architecture

NyayaTrace supplies database credentials through three primary channels:

### A. Docker Compose Infrastructure
- **`compose.yaml` (Base experiment container):**
  - Requires `POSTGRES_PASSWORD` via environment variable or standard root `.env`:
    ```yaml
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in .env}
    ```
  - Port binding: `127.0.0.1:54329:5432`.
- **`compose.demo.yaml` (Interactive research demo):**
  - Synthesizes `LEGAL_XAI_DATABASE_URL` dynamically from Compose environment:
    ```yaml
    LEGAL_XAI_DATABASE_URL: postgresql://legal_xai:${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD in the environment}@postgres:5432/legal_xai
    ```
  - Port binding: `127.0.0.1:54330:5432`.

### B. Python Tooling & Verification Scripts
- Scripts throughout `scripts/` utilize standard environment variable resolution:
  ```python
  parser.add_argument("--database-url", default=os.getenv("LEGAL_XAI_DATABASE_URL", DEFAULT_DATABASE_URL))
  ```
- As documented in `FINAL_VALIDATION_PREP.md`, external callers supply credentials via standard shell environment variables:
  ```powershell
  $env:LEGAL_XAI_DATABASE_URL = "postgresql://legal_xai:[REDACTED]@127.0.0.1:54329/legal_xai"
  ```

### C. Containerized Replay Architecture
- During the Phase 16 audit replay, the `nyayatrace-e2` container required network access to the host's PostgreSQL instance. On Windows Docker Desktop, this requires routing to `host.docker.internal:54329`.
- To avoid hardcoding credentials in command lines, `experiments/audit_fixes/replay/.db_env` was passed via `docker run --env-file`.
- The replay completed successfully (`e3e4_replay.json` generated, `e3e4_replay_gpu3.log` verified).

---

## 2. Runtime Necessity Determination

| Channel | Requires `.db_env`? | Alternative Mechanism |
|:---|:---|:---|
| **Active Postgres Service** | No | Managed via Compose / Docker Daemon |
| **Python CLI Tools** | No | Uses `$env:LEGAL_XAI_DATABASE_URL` directly |
| **Connected Demo** | No | Configured via `compose.demo.yaml` |
| **Future Replay Execution** | No | Pass `-e LEGAL_XAI_DATABASE_URL=...` or standard root `.env` |

### Verdict
`experiments/audit_fixes/replay/.db_env` is **NOT** a runtime necessity. It is a leftover artifact from the containerized replay execution.
