# AppSail full endpoint validation

**Base URL:** `https://crimematrix-ai-50044181811.development.catalystappsail.in`
**When:** 2026-07-26 11:27:00

| PASS | BLOCK (backend) | FAIL | TOTAL |
|------|-----------------|------|-------|
| 85 | 1 | 4 | 90 |

| Result | Tier | Endpoint | Status | Time | Notes |
|--------|------|----------|--------|------|-------|
| PASS | A | `GET /docs` | 200 | 0.2s |  |
| PASS | A | `GET /health` | 200 | 0.2s |  |
| PASS | A | `GET /models` | 200 | 0.3s |  |
| PASS | A | `GET /agents` | 200 | 0.1s |  |
| PASS | A | `GET /agents/default` | 200 | 0.1s |  |
| PASS | A | `GET /sessions` | 200 | 0.1s |  |
| PASS | A | `GET /tools` | 200 | 0.2s |  |
| PASS | A | `GET /tools/calculator` | 200 | 0.1s |  |
| PASS | A | `GET /prompts` | 200 | 0.1s |  |
| PASS | A | `GET /tokens` | 200 | 0.1s |  |
| PASS | A | `GET /workflows` | 200 | 0.1s |  |
| PASS | B | `GET /workflows/investigation` | 200 | 0.1s |  |
| PASS | B | `GET /workflows/investigation/steps` | 200 | 0.1s |  |
| PASS | A | `POST /chat` | 200 | 1.5s |  |
| PASS | A | `POST /tools/invoke:calculator` | 200 | 0.1s |  |
| FAIL | B | `GET /memory/sessions/full-validate/history` | 500 | 0.2s | Internal Server Error |
| FAIL | B | `GET /memory/sessions/full-validate/summary` | 500 | 0.1s | Internal Server Error |
| PASS | B | `GET /memory/preferences/validate-user` | 200 | 0.1s |  |
| PASS | B | `PUT /memory/preferences/validate-user` | 200 | 0.1s |  |
| PASS | B | `GET /memory/working` | 200 | 0.1s |  |
| BLOCK | C | `POST /memory/investigation` | 200 | 0.1s | expected (needs backend) |
| PASS | B | `DELETE /sessions/full-validate-del` | 200 | 0.2s |  |
| PASS | B | `GET /sessions/full-validate/trace` | 200 | 0.1s |  |
| PASS | C | `POST /rag/index` | 200 | 0.1s |  |
| PASS | B | `POST /rag/search` | 200 | 0.1s |  |
| PASS | B | `GET /rag/stats` | 200 | 0.1s |  |
| PASS | B | `GET /rag/citations/full-validate` | 200 | 0.1s |  |
| PASS | B | `POST /search/expand` | 200 | 3.0s |  |
| PASS | B | `POST /search/rewrite` | 200 | 1.2s |  |
| PASS | B | `POST /search/rerank` | 200 | 0.2s |  |
| PASS | B | `POST /search/intelligent` | 200 | 0.2s |  |
| PASS | C | `POST /search/similar` | 200 | 0.1s |  |
| PASS | C | `POST /search/cross-district` | 200 | 0.1s |  |
| PASS | B | `GET /search/stats` | 200 | 0.1s |  |
| PASS | A | `POST /identity/match` | 200 | 0.1s |  |
| PASS | B | `POST /identity/match/batch` | 200 | 0.1s |  |
| PASS | A | `POST /identity/transliterate` | 200 | 0.1s |  |
| PASS | B | `POST /identity/duplicates` | 200 | 0.1s |  |
| PASS | B | `POST /identity/resolve` | 200 | 0.1s |  |
| PASS | B | `POST /identity/merge` | 200 | 0.1s |  |
| PASS | B | `POST /identity/aliases` | 200 | 0.1s |  |
| PASS | B | `GET /identity/stats` | 200 | 0.1s |  |
| PASS | C | `POST /knowledge/build` | 200 | 0.2s |  |
| PASS | B | `POST /knowledge/query` | 200 | 0.1s |  |
| PASS | B | `POST /knowledge/network` | 200 | 0.6s |  |
| PASS | B | `POST /knowledge/discover` | 200 | 0.1s |  |
| PASS | B | `POST /knowledge/timeline` | 200 | 0.1s |  |
| PASS | B | `POST /knowledge/analyze` | 200 | 0.1s |  |
| PASS | B | `GET /knowledge/stats` | 200 | 0.1s |  |
| PASS | B | `POST /reasoning/chain` | 200 | 0.1s |  |
| PASS | B | `POST /reasoning/evidence` | 200 | 0.1s |  |
| PASS | B | `POST /reasoning/confidence` | 200 | 0.1s |  |
| PASS | B | `POST /reasoning/analyze` | 200 | 8.5s |  |
| PASS | B | `POST /reasoning/explain` | 200 | 12.2s |  |
| FAIL | B | `POST /predict/forecast` | 500 | 0.2s | Internal Server Error |
| PASS | B | `POST /predict/hotspots` | 200 | 0.1s |  |
| PASS | B | `POST /predict/recidivism` | 200 | 0.1s |  |
| PASS | B | `POST /predict/risk` | 200 | 0.1s |  |
| PASS | B | `POST /predict/mo-similarity` | 200 | 0.1s |  |
| PASS | B | `POST /predict/cases` | 200 | 0.1s |  |
| PASS | B | `GET /predict/stats` | 200 | 0.1s |  |
| PASS | B | `POST /language/stt` | 200 | 0.1s |  |
| PASS | B | `POST /language/tts` | 200 | 0.1s |  |
| PASS | B | `POST /language/translate` | 200 | 0.1s |  |
| PASS | A | `POST /language/kanglish` | 200 | 0.2s |  |
| PASS | A | `POST /language/normalize` | 200 | 0.1s |  |
| FAIL | B | `GET /language/stats` | 500 | 0.1s | Internal Server Error |
| PASS | A | `POST /embeddings/embed` | 200 | 0.1s |  |
| PASS | B | `POST /embeddings/similarity` | 200 | 0.1s |  |
| PASS | B | `POST /embeddings/batch` | 200 | 0.1s |  |
| PASS | B | `POST /embeddings/search` | 200 | 0.1s |  |
| PASS | B | `GET /embeddings/stats` | 200 | 0.1s |  |
| PASS | B | `POST /workflows/run` | 200 | 0.1s |  |
| PASS | B | `GET /models/registry` | 200 | 0.2s |  |
| PASS | B | `GET /models/registry/conversation` | 200 | 0.1s |  |
| PASS | B | `GET /models/config` | 200 | 0.1s |  |
| PASS | B | `POST /models/registry` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/latency` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/tokens` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/hallucination` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/tools` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/accuracy` | 200 | 0.4s |  |
| PASS | B | `GET /monitor/confidence` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/cost` | 200 | 0.1s |  |
| PASS | B | `POST /monitor/feedback` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/feedback` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/dashboard` | 200 | 0.1s |  |
| PASS | B | `GET /monitor/summary` | 200 | 0.1s |  |
| PASS | C | `POST /tools/invoke:crime_search` | 200 | 0.2s |  |
| PASS | C | `POST /tools/invoke:similar_cases` | 200 | 0.2s |  |

## Interpretation

- **PASS** — works on AppSail alone (OpenRouter + in-process logic).
- **BLOCK** — needs `BACKEND_URL` (CrimeMatrix backend not deployed yet).
- **FAIL** — unexpected; investigate.
