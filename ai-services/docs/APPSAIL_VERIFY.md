# AppSail verification notes

## Tier A — must pass (no backend)

Covered by `scripts/smoke_appsail.py`.

## Tier B — should pass (in-process)

Identity match/resolve, reasoning/*, predict/* heuristics, rag/search (empty OK),
knowledge/* (empty graph OK), monitor/*, memory/*, search/rewrite|expand.

## Tier C — expected fail until backend is deployed

These call `BACKEND_URL` (default `http://localhost:8001`). On AppSail that host
is unreachable until the CrimeMatrix backend is deployed and `BACKEND_URL` is set
in the AppSail environment.

| Area | Examples |
|------|----------|
| Crime tools | `crime_search`, `crime_detail`, `crime_list`, `crime_stats` |
| Investigation | notes, timeline, status, analyze |
| Similar / patterns | similar cases, pattern detect, recommendations |
| Prediction tools that fetch cases | forecast, risk, priority (when they load from API) |
| Alerts / evaluation / explain | early warning, evaluation report, explain insight |
| Persistence helpers | graph/memory/embeddings persistence against backend |

Failures here are **not** AppSail regressions — they are blocked on backend deploy.
