# Demo-stack scope conformance (connected React + Spring + FastAPI)

Maintenance note for the scope audit: the three-layer connected demo required
by the canonical specification is implemented here. Research pipeline,
datasets, checkpoints, metrics, RQs, paper, and freeze are untouched.

| Required item | Status | Evidence |
|---|---|---|
| React/TypeScript frontend | IMPLEMENTED | `demo/web/` (`package.json` react 18 + TS + vite, `src/App.tsx`, `src/api.ts`, `src/types.ts`) |
| Spring Boot API | IMPLEMENTED | `demo/spring-api/` (`pom.xml` Boot 3.2.5/Java 17, `controller/`, `service/`, `client/`, `config/`, `model/`, `audit/`) |
| Python/FastAPI ML service | IMPLEMENTED | `demo/ml-service/app.py` (`GET /health`, `POST /research/query`; delegates to `src/legal_xai`, no duplicated logic) |
| Authentication (local demo) | IMPLEMENTED | `AuthFilter.java` (Bearer vs `DEMO_API_TOKEN`, fail-closed) + FastAPI `X-Internal-Token` vs `ML_INTERNAL_TOKEN`; `.env` ignored, compose guards (`${VAR:?…}`), no committed secrets |
| Audit endpoint | IMPLEMENTED | `GET /api/audit/{requestId}` over bounded in-memory `AuditStore` (request/timestamp/experiment/model+index versions/query/evidence IDs/verification/temporal/status; no personal data, no secrets) |
| Experiment metadata endpoint | IMPLEMENTED | `GET /api/experiments` serves `experiments.json` (E1–E4 purpose/status/config/result references; no new experiments) |
| React→Spring→FastAPI integration | IMPLEMENTED | `ResearchService` forwards frozen E4 path; `MlClientContractTest` pins URL/header/body contract; FastAPI smoke covers envelope wiring |
| Static demo preserved | IMPLEMENTED | `demo/index.html`, `app.mjs`, `data.mjs`, `verify.mjs` untouched; still served by `scripts/serve_week16_demo.py` as the frozen-artifact viewer/fallback |

Explicit non-claims: local loopback deployment only (no production/SaaS/K8s/multi-tenancy); no autonomous decisions; provenance is traceability, not legal correctness; predictions experimental; uncertainty generic.
