# AppSail deploy — CrimeMatrix Backend

## Live URL

After first deploy, Catalyst assigns a host like:

**https://crimematrix-backend-&lt;project&gt;.development.catalystappsail.in**

| Item | Value |
|------|--------|
| Project | Project-Rainfall (`46575000000013023`) |
| Org | `60079208195` |
| AppSail | `crimematrix-backend` |
| Recommended memory | **512 MB** |

## Console env (required once)

Custom AppSail **cannot** receive secrets from the CLI. Set them in the console:

1. [Catalyst Console (IN)](https://console.catalyst.zoho.in/) → **Project-Rainfall**
2. **Serverless → AppSail → crimematrix-backend**
3. If Inactive: **⋯ → Enable**
4. **Configuration** → Memory **512 MB** + env:

| Key | Value |
|-----|--------|
| `DB_PROVIDER` | `catalyst` |
| `CATALYST_PROJECT_ID` | `46575000000013023` |
| `CATALYST_ORG_ID` | `60079208195` |
| `CATALYST_ENVIRONMENT` | `Development` |
| `CATALYST_API_DOMAIN` | `https://api.catalyst.zoho.in` |
| `CATALYST_ACCOUNTS_DOMAIN` | `https://accounts.zoho.in` |
| `CATALYST_CLIENT_ID` | *(from `backend/.env`)* |
| `CATALYST_CLIENT_SECRET` | *(from `backend/.env`)* |
| `CATALYST_REFRESH_TOKEN` | *(from `backend/.env`)* |
| `CATALYST_FILE_FOLDER_ID` | *(File Store folder id)* |
| `AI_SERVICES_URL` | `https://crimematrix-ai-50044181811.development.catalystappsail.in` |
| `STORAGE_PROVIDER` | `catalyst` |

5. Save; wait ~30–60s for a new instance.

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
