# AppSail deploy — CrimeMatrix Backend

## Live URL

**https://crimematrix-backend-50044181811.development.catalystappsail.in**

| Item | Value |
|------|--------|
| Project | Project-Rainfall (`46575000000013023`) |
| Org | `60079208195` |
| AppSail | `crimematrix-backend` |
| Recommended memory | **512 MB** |

## Console env (required once)

Custom AppSail **cannot** receive secrets from the CLI. Set them in the console.

**Important:** AppSail rejects custom env keys named `CATALYST_*` (platform-reserved).
Use the `CM_*` names below. Local `backend/.env` may still use `CATALYST_*`; the app
reads `CM_*` first, then falls back.

1. [Catalyst Console (IN)](https://console.catalyst.zoho.in/) → **Project-Rainfall**
2. **Serverless → AppSail → crimematrix-backend**
3. If Inactive: **⋯ → Enable**
4. **Configuration** → Memory **512 MB** + env:

| Key | Value |
|-----|--------|
| `DB_PROVIDER` | `catalyst` |
| `CM_PROJECT_ID` | `46575000000013023` |
| `CM_ORG_ID` | `60079208195` |
| `CM_ENVIRONMENT` | `Development` |
| `CM_API_DOMAIN` | `https://api.catalyst.zoho.in` |
| `CM_ACCOUNTS_DOMAIN` | `https://accounts.zoho.in` |
| `CM_CLIENT_ID` | *(from `backend/.env`)* |
| `CM_CLIENT_SECRET` | *(from `backend/.env`)* |
| `CM_REFRESH_TOKEN` | *(from `backend/.env`)* |
| `CM_FILE_FOLDER_ID` | *(File Store folder id)* |
| `AI_SERVICES_URL` | `https://crimematrix-ai-50044181811.development.catalystappsail.in` (**origin only** — no `/api/ai`) |
| `STORAGE_PROVIDER` | `catalyst` |

5. Save; wait ~30–60s for a new instance.

Paste-ready lines (reads local `.env` via `CM_*` or legacy `CATALYST_*`):

```bash
cd backend
python scripts/print_appsail_env.py
```

Also set on **crimematrix-ai**:

| Key | Value |
|-----|--------|
| `BACKEND_URL` | `https://crimematrix-backend-50044181811.development.catalystappsail.in` |

## Rebuild + redeploy

```powershell
cd backend
docker build -t crimematrix-backend:latest .
docker save crimematrix-backend:latest -o crimematrix-backend.tar

cd ../catalyst
$env:ZCATALYST_NON_INTERACTIVE = "1"
catalyst deploy appsail `
  --name crimematrix-backend `
  --source "docker-archive://D:/projects/website/crimematrix/backend/crimematrix-backend.tar" `
  --command "sh -c 'uvicorn main:app --host 0.0.0.0 --port `${X_ZOHO_CATALYST_LISTEN_PORT}'" `
  --port 9000 `
  --org 60079208195 `
  -p 46575000000013023 `
  -ni
```

Re-check console memory + env after redeploy (memory may reset to 2048).

## Smoke

```bash
curl https://<backend-host>/api/v1/health
curl https://<backend-host>/api/v1/districts
curl https://<backend-host>/api/v1/crimes
```

Expect Catalyst-seeded districts/crimes when `DB_PROVIDER=catalyst` and OAuth env are set.

Print paste-ready env (secrets from local `.env`):

```bash
cd backend
python scripts/print_appsail_env.py
```
