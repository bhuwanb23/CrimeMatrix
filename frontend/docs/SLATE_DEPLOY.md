# Slate deploy — CrimeMatrix Frontend

## Live URL

**https://crimematrix-frontend-nvjwdioh.onslate.in**

| Item | Value |
|------|--------|
| Project | Project-Rainfall (`46575000000013023`) |
| Org | `60079208195` |
| Slate app | `crimematrix-frontend` |
| Framework | React + Vite |
| Build output | `dist/` |

## Bake-time API URL

Vite embeds env at **build** time. Tracked production values live in [`frontend/.env.production`](../.env.production):

```
VITE_API_URL=https://crimematrix-backend-50044181811.development.catalystappsail.in/api/v1
VITE_AI_URL=https://crimematrix-ai-50044181811.development.catalystappsail.in/api/ai
```

Only `VITE_API_URL` is used by the app (`src/services/api.js`). It must include `/api/v1`.

## Link (once per machine / after cloning)

`catalyst/` is local-only (gitignored). From the Catalyst project directory:

```powershell
cd D:\projects\website\crimematrix\catalyst
$env:ZCATALYST_NON_INTERACTIVE = "1"
catalyst slate:link `
  --name crimematrix-frontend `
  --framework "React + Vite" `
  --source "D:/projects/website/crimematrix/frontend" `
  -ni
```

Expected `catalyst.json` slate entry:

```json
"slate": [
  {
    "name": "crimematrix-frontend",
    "source": "D:\\projects\\website\\crimematrix\\frontend"
  }
]
```

Defaults (auto-detected): install `npm install`, build `npm run build`, output `/dist`.

## Redeploy

```powershell
cd D:\projects\website\crimematrix\catalyst
$env:ZCATALYST_NON_INTERACTIVE = "1"
catalyst deploy slate crimematrix-frontend -m "frontend update" -ni
```

Slate builds remotely from the linked source (runs `npm install` + `npm run build` with `.env.production`).

## CORS notes

AppSail’s edge answers OPTIONS without CORS headers. The frontend therefore:

- Omits `Content-Type` on body-less GETs/DELETEs so they stay simple requests (no preflight)
- Relies on backend `CORSMiddleware` reflecting the Slate origin (`*.onslate.in` + localhost)

Backend CORS is configured in `backend/main.py` (`allow_credentials=False`, explicit origins / regex).

If POSTs (JSON) start failing preflight from a new Slate URL, either update backend `allow_origins` / regex and redeploy AppSail, or whitelist the domain under Catalyst **Authentication → Whitelisting → Authorized Domains** (CORS enabled).

## Smoke

```powershell
cd D:\projects\website\crimematrix\frontend
python scripts/smoke_slate.py
```

Manual: open the Slate URL, confirm dashboard API calls return 200, refresh `/copilot` (SPA fallback).

## Local vs Slate

| Mode | How |
|------|-----|
| Local Vite → live APIs | Copy `.env.catalyst` → `.env.local`, then `npm run dev` |
| Slate (hosted) | Deploy as above; uses `.env.production` |
