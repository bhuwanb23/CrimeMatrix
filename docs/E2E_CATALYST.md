# CrimeMatrix E2E on Catalyst (Backend + DB + AI)

Date: 2026-07-26 (verified after `CM_*` console env)

## Live URLs

| Service | URL |
|---------|-----|
| Backend AppSail | https://crimematrix-backend-50044181811.development.catalystappsail.in |
| AI AppSail | https://crimematrix-ai-50044181811.development.catalystappsail.in |
| Frontend (local) | `frontend/.env.local` from `.env.catalyst` → `VITE_API_URL` → backend `/api/v1` |

## Phase 1 Data Store

- Tables: **35/35** created and seeded
- Smoke (`python -m catalyst_datastore.smoke_test --provider catalyst`): **5/5 PASS**

## Verification results (post-env)

### Backend AppSail

| Check | Result |
|-------|--------|
| `GET /api/v1/health` | **PASS** |
| `GET /api/v1/config` | **PASS** — `db_provider=catalyst`, `ai_services_url` normalized to AI origin |
| `GET /api/v1/districts/?page=1&page_size=3` | **PASS** — Catalyst data (e.g. Bengaluru Urban) |
| `GET /api/v1/crimes/?page=1&page_size=3` | **PASS** — seeded crimes |
| `POST /api/v1/search/` `{"query":"theft"}` | **PASS** — matches from Data Store |
| `POST /api/v1/copilot/chat` | **PASS** — proxies to live AI |

### AI AppSail ↔ Backend

| Check | Result |
|-------|--------|
| `GET /api/ai/health` | **PASS** (OpenRouter, 34 tools) |
| `POST /api/ai/tools/invoke` `crime_search` | **PASS** — e.g. 7 theft hits from backend |
| `POST /api/ai/tools/invoke` `crime_stats` | **PASS** — Phase 1 overview via backend |
| `POST /api/ai/chat` with tools | **PASS** — tool path reaches backend |

### Env notes

- AppSail custom keys must be **`CM_*`**, not `CATALYST_*` (reserved).
- `AI_SERVICES_URL` / `BACKEND_URL` must be **host origins** (no `/api/ai` or `/api/v1`). Trailing path suffixes are stripped automatically by the backend.
- Prefer trailing slash or query on list routes (`/districts/?page=1`) — bare `/districts` can 400 via the AppSail proxy.

## Frontend

```bash
cd frontend && npm run dev
```

## Deploy docs

- Backend: [`backend/docs/APPSAIL_DEPLOY.md`](../backend/docs/APPSAIL_DEPLOY.md)
- AI: [`ai-services/docs/APPSAIL_DEPLOY.md`](../ai-services/docs/APPSAIL_DEPLOY.md)

## Non-goals (unchanged)

- Full ML/intel table migration
- Catalyst Authentication / API Gateway
- Frontend visual redesign
