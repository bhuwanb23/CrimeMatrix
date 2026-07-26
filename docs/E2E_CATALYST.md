# CrimeMatrix E2E on Catalyst (Backend + DB + AI)

Date: 2026-07-26

## Live URLs

| Service | URL |
|---------|-----|
| Backend AppSail | https://crimematrix-backend-50044181811.development.catalystappsail.in |
| AI AppSail | https://crimematrix-ai-50044181811.development.catalystappsail.in |
| Frontend (local) | set `frontend/.env.local` from `.env.catalyst` → `VITE_API_URL` → backend `/api/v1` |

## Phase 1 Data Store

- Tables: **35/35** created
- Seed: **35/35** touched (includes `witnesses`, `case_links`, `case_status_logs`, `attachments`)
- Smoke (`python -m catalyst_datastore.smoke_test --provider catalyst`): **5/5 PASS**
- Schema quirks documented in [`docs/CATALYST_DATASTORE.md`](CATALYST_DATASTORE.md):
  - `states.code` live as bigint
  - `investigations.district` may be missing

## Verification results

### Backend AppSail

| Check | Result |
|-------|--------|
| `GET /api/v1/health` | **PASS** (`healthy`) |
| `GET /api/v1/districts/?page=1&page_size=5` | **PASS** (200; empty until console sets `DB_PROVIDER=catalyst` + `CM_*` OAuth) |
| `GET /api/v1/districts` (no slash) | 400 via AppSail proxy (use trailing `/` or query) |
| Image start (local docker, sqlite) | **PASS** |

### AI AppSail

| Check | Result |
|-------|--------|
| `GET /api/ai/health` | **PASS** (OpenRouter true, 34 tools) |
| `POST /api/ai/chat` (theft search) | **PASS** HTTP 200; tool path soft-fails until `BACKEND_URL` is set in **crimematrix-ai** console |

### Local Catalyst provider (OAuth from `backend/.env`)

| Table | Seeded rows visible |
|-------|---------------------|
| districts / crimes / notes | yes |
| witnesses / attachments | yes |

## Console wiring still required (cannot set via CLI for custom images)

Paste env with:

```bash
cd backend
python scripts/print_appsail_env.py
```

Use **`CM_*` keys only** in AppSail (not `CATALYST_*` — reserved).

1. **crimematrix-backend** → Configuration → env from script output + Memory **512 MB**
2. **crimematrix-ai** → add `BACKEND_URL=https://crimematrix-backend-50044181811.development.catalystappsail.in`
3. Wait ~60s, then re-check:

```bash
curl "https://crimematrix-backend-50044181811.development.catalystappsail.in/api/v1/districts/?page=1&page_size=5"
curl -X POST "https://crimematrix-ai-50044181811.development.catalystappsail.in/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"search crimes about theft","use_tools":true,"user_id":"e2e"}'
```

Expect districts/crimes non-empty from Data Store, and chat tools no longer connection-failing to backend.

## Frontend

```bash
# already generated
# frontend/.env.local  (from .env.catalyst)
cd frontend && npm run dev
```

`VITE_API_URL` points at the live backend AppSail `/api/v1`.

## Deploy docs

- Backend: [`backend/docs/APPSAIL_DEPLOY.md`](../backend/docs/APPSAIL_DEPLOY.md)
- AI: [`ai-services/docs/APPSAIL_DEPLOY.md`](../ai-services/docs/APPSAIL_DEPLOY.md)

## Non-goals (unchanged)

- Full ML/intel table migration
- Catalyst Authentication / API Gateway
- Frontend visual redesign
