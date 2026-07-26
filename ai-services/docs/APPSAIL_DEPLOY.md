# AppSail deploy — CrimeMatrix AI Services

## Live URL

**https://crimematrix-ai-50044181811.development.catalystappsail.in**

| Item | Value |
|------|--------|
| Project | Project-Rainfall (`46575000000013023`) |
| Org | `60079208195` |
| AppSail | `crimematrix-ai` |
| Image size | ~636 MB (no Torch) / tar ~139 MB |
| Recommended memory | **512 MB** |

## Do this once in the Catalyst console (required)

Custom AppSail **cannot** receive secrets from the CLI. Set them in the console:

1. Open [Catalyst Console (IN)](https://console.catalyst.zoho.in/) → project **Project-Rainfall**
2. **Serverless → AppSail → crimematrix-ai**
3. If status is Inactive: **⋯ → Enable**
4. **Configuration**:
   - Memory: **512 MB** (CLI custom deploy defaults to 2048 MB — change this to cut cost)
   - Environment variables (Development):

| Key | Value |
|-----|--------|
| `OPENROUTER_API_KEY` | *(copy from local `ai-services/.env` — never commit)* |
| `OPENROUTER_MODEL` | `meta-llama/llama-3.1-8b-instruct` |
| `EMBEDDING_BACKEND` | `tfidf` |
| `BACKEND_URL` | `https://crimematrix-backend-50044181811.development.catalystappsail.in` |

5. Save and wait ~30–60 seconds for a new instance.

## Verify

```bash
python ai-services/scripts/smoke_appsail.py --base https://crimematrix-ai-50044181811.development.catalystappsail.in
```

Without `OPENROUTER_API_KEY`, Tier A chat fails (falls back to Ollama, which is not on AppSail). Other Tier A GETs already pass.

## Rebuild + redeploy

```powershell
cd ai-services
docker build -t crimematrix-ai:latest .
docker save crimematrix-ai:latest -o crimematrix-ai.tar

cd ../catalyst
$env:ZCATALYST_NON_INTERACTIVE = "1"
catalyst deploy appsail `
  --name crimematrix-ai `
  --source "docker-archive://D:/projects/website/crimematrix/ai-services/crimematrix-ai.tar" `
  --command "sh -c 'uvicorn main:app --host 0.0.0.0 --port `${X_ZOHO_CATALYST_LISTEN_PORT}'" `
  --port 9000 `
  --org 60079208195 `
  -p 46575000000013023 `
  -ni
```

Then re-check console memory + env vars (redeploy may reset memory to 2048).

## Resource choices (why this is lean)

- Dropped Torch / `sentence-transformers` for AppSail (`requirements-appsail.txt`)
- Embeddings use TF-IDF (already the domain embedder path); MiniLM forced off via `EMBEDDING_BACKEND=tfidf`
- 512 MB RAM is enough for FastAPI + sklearn; avoid 2048 MB unless you re-add Torch
