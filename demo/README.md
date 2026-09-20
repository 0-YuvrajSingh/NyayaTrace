# Week 16 minimal researcher demo

From the repository root, run:

```powershell
python scripts/serve_week16_demo.py
```

Open http://127.0.0.1:8000/demo/ and stop with Ctrl+C. No npm install, model weights, PostgreSQL, or pipeline execution is needed.

This is the frozen plan's minimal researcher-facing interface: a single-user local demo, not a production system. It has no accounts, arbitrary-query retrieval, or deployment infrastructure.

All seven Week 13 examples are included: 2008_1629, 1980_105, 1980_133, 1981_55, 1985_40, 1997_792, and 2013_35. Select a case and switch between structured and unstructured presentations.

The browser reads `artifacts/week13_review_packet.md` for the frozen excerpt, authorities, passages, conclusion, and uncertainty. The final `artifacts/week11_temporal_prerank_evaluation.json` has citation checks and outcome flags but does not contain the full answer text. `artifacts/week13_rq3_ablation_parity.json` supplies the independent packet citation-ID mapping. No older pre-fix answer is substituted and no review ratings are shown. Before displaying anything, the page checks both presentations' ordered citation IDs and reporter citations against the evaluation, and checks passage parity across formats. Original text, including OCR imperfections, is preserved.

The launcher serves only the three artifacts above and the demo HTML/CSS/modules on loopback. It does not expose the workspace, credentials, models, or database. Run `node demo/verify.mjs` to verify all seven examples offline.

## Verification

Verified all seven cases in both formats in headless Microsoft Edge: 14 rendered displays, 35/35 ordered citation IDs and reporter citations per format, and unchanged verbatim passages. The structured view exposes all five sections. Desktop and 390-pixel mobile layout checks pass, with no browser script errors. A screenshot is saved at `artifacts/week16_demo.png`.

Optional browser verification (Playwright is a development-only tool, not required to run the demo):

```powershell
# In a separate terminal, keep the demo running on port 8016:
python scripts/serve_week16_demo.py --port 8016
# Then, in another terminal at the repository root:
$demoTools = Join-Path $env:TEMP 'legal-xai-demo-browser-tools'
npm install --prefix $demoTools playwright --no-audit --no-fund
$env:DEMO_PLAYWRIGHT_MODULE = Join-Path $demoTools 'node_modules/playwright/index.mjs'
node demo/verify-browser.mjs
```

This verification uses an installed Microsoft Edge browser and checks the actual rendered passages and citations against the packet/evaluation. It also checks that paths outside the demo allowlist return 404.

---

# Connected demo stack (React + Spring Boot + FastAPI, local research only)

The static viewer above is preserved as the frozen-artifact viewer and fallback.
The connected stack adds the specification-required three layers over the
**unchanged** research pipeline (`src/legal_xai`, frozen configs, BM25 index,
provenance database, E2 checkpoint). No scientific logic was modified.

## Architecture

```text
React web (demo/web, :8081)
  ↓ GET /api/* with Bearer DEMO_API_TOKEN
Spring Boot API (demo/spring-api, :8080)
  ↓ POST /research/query with X-Internal-Token
FastAPI ML service (demo/ml-service, :8001)
  ↓ existing facts → salient query → temporal pre-rank BM25 → selection
    → provenance → citation verification → extract-only explanation
    (+ frozen-ckpt prediction only when GPU + checkpoint available)
```

Request / response flow returns the structured E4 result (issue, authorities,
verbatim evidence + provenance, temporal status, citation verification,
experimental prediction or skipped reason, uncertainty, human-review notice).

## Prerequisites

- Docker Desktop (for the full stack), or Node 20 + Java 17 + Maven + Python 3.11 for native runs.
- Local assets already required by the reproducibility record: `retrieval/bm25.sqlite`,
  `corpus/dedup_matches.csv`, E2 `checkpoint-6318` (read-only binds), and a PostgreSQL
  provenance database (the demo compose file creates a separate throwaway volume;
  load it with `scripts/load_provenance.py` pointed at port 54330 if needed).

## Environment variables (never commit values; `.env` stays ignored)

| Variable | Used by | Purpose |
|---|---|---|
| `POSTGRES_PASSWORD` | compose | demo database password (required, `${VAR:?…}` guard) |
| `DEMO_API_TOKEN` | Spring, web UI field | browser → API bearer token (required; empty = all protected calls 401) |
| `ML_INTERNAL_TOKEN` | Spring → FastAPI | internal caller token (required; empty = FastAPI research endpoint open locally) |
| `LEGAL_XAI_DATABASE_URL` | FastAPI | provenance DB URL (defaults to the documented local default) |

## Startup / shutdown

```powershell
# Repository root. No secrets are stored anywhere by these commands.
$env:POSTGRES_PASSWORD = "local-only-dev"
$env:DEMO_API_TOKEN = "local-only-dev"
$env:ML_INTERNAL_TOKEN = "local-only-dev"
docker compose -f compose.demo.yaml up --build
# UI: http://127.0.0.1:8081/  (API: :8080, ML: :8001, demo DB: 127.0.0.1:54330)
# Enter the same DEMO_API_TOKEN value in the UI token field.
docker compose -f compose.demo.yaml down  # leaves the research volume alone
```

Native alternative (three terminals): `uvicorn app:app` in `demo/ml-service`
(`PYTHONPATH=src`), `mvn spring-boot:run` in `demo/spring-api` (with env set),
`npm install; npm run dev` in `demo/web`.

## Example research request

```powershell
$headers = @{ Authorization = "Bearer local-only-dev" }
$body = @{ query = "anticipatory bail section 438"; query_id = "week10-replay-01";
           query_year = 2020; candidate_k = 100; top_k = 5 } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8080/api/research/query -Method Post `
  -Headers $headers -Body $body -ContentType "application/json"
```

## API endpoints

| Method + path | Auth | Purpose |
|---|---|---|
| `GET /api/health` | open | API liveness + ML reachability (`ml_status`) |
| `POST /api/research/query` | Bearer | E4 evidence path; `{request_id, result}` envelope |
| `GET /api/experiments` | Bearer | E1–E4 metadata references (no new experiments) |
| `GET /api/audit/{requestId}` | Bearer | Minimal audit record for one request |
| `GET /health` (ML, :8001) | open | asset readiness (index/dedup/configs/checkpoint/CUDA flags) |
| `POST /research/query` (ML, :8001) | internal token if configured | same E4 path, direct |

## Research pipeline vs demo layer

- Research pipeline (`src/`, `scripts/`, `config/`, corpora, index, checkpoint,
  frozen results): unchanged and authoritative; the demo only calls it.
- Demo layer (`demo/web`, `demo/spring-api`, `demo/ml-service`,
  `compose.demo.yaml`): orchestration + presentation only; no BM25/provenance/model
  logic re-implemented in Java or TypeScript.

This demo is not production-ready: loopback-only, single shared local token, bounded
in-memory audit (500 records), no multi-tenancy, no Kubernetes, no enterprise security.
Scope conformance details: `demo/SCOPE_CONFORMANCE_DEMO.md`.
