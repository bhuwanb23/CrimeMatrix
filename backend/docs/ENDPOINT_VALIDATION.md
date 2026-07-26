# Backend endpoint validation

- Base: `https://crimematrix-backend-50044181811.development.catalystappsail.in`
- Generated: `2026-07-26T10:11:09.742760+00:00`
- Total operations: **461**
- PASS: **384**
- SOFT: **23** (empty/validation/missing-id/expected AppSail gaps)
- FAIL: **26** (HTTP 500 — see categories below)
- SKIP: **28** (destructive deletes / multipart / SSE streams)

## Verdict

**Core Phase-1 + AI-critical reads are healthy.** Failures cluster in three areas that were deferred or still on SQLAlchemy create paths:

| Category | Count | Examples | Notes |
|----------|------:|----------|-------|
| Graph store | 12 | `/graph/nodes`, `/graph/edges`, `/graph/timeline` | In-memory/SQLite graph not initialized on AppSail; Phase-2 deferred |
| SQLAlchemy creates (not Catalyst write) | 9 | `POST /districts/`, `/cases/`, `/officers/`, `/stations/`, `/vehicles/`, `/victims/`, `/crime-types/`, `/timeline/`, `/datastore/districts` | List/GET use Catalyst; create still hits empty SQLite schema |
| Analytics / intel detectors | 4 | `/analytics/timeseries/*`, `/cross-district/detect`, `/evidence-linking/detect` | SQLite/ML paths; soft-empty preferred later |
| Storage download probe | 1 | `/storage/download/{bad}` | Bad path probe |

**Phase-1 GET lists that passed:** districts, crimes, cases, investigations, criminals, officers, persons, suspects, stations, vehicles, locations, crime-types, witnesses, notes, timeline, case-status, search, analytics overview, copilot chat, config, health, and most ML GET stubs returning 200 empty.

Re-run:

```bash
cd backend
python scripts/validate_all_endpoints.py
```

## FAIL details

| Method | Path | Status | Detail |
|--------|------|--------|--------|
| GET | `/api/v1/analytics/timeseries/activity` | 500 | Internal server error |
| GET | `/api/v1/analytics/timeseries/crimes` | 500 | Internal server error |
| POST | `/api/v1/cases/` | 500 | Internal server error |
| POST | `/api/v1/crime-types/` | 500 | Internal server error |
| POST | `/api/v1/cross-district/detect` | 500 | Internal server error |
| POST | `/api/v1/datastore/districts` | 500 | Internal server error |
| POST | `/api/v1/districts/` | 500 | Internal server error |
| POST | `/api/v1/evidence-linking/detect` | 500 | Internal server error |
| GET | `/api/v1/graph/edges` | 500 | Internal server error |
| GET | `/api/v1/graph/edges/1` | 500 | Internal server error |
| DELETE | `/api/v1/graph/edges/46575000000050045/46575000000050045` | 500 | Internal server error |
| GET | `/api/v1/graph/neighbors/1` | 500 | Internal server error |
| GET | `/api/v1/graph/nodes` | 500 | Internal server error |
| GET | `/api/v1/graph/nodes/search/46575000000050045` | 500 | Internal server error |
| DELETE | `/api/v1/graph/nodes/1` | 500 | Internal server error |
| GET | `/api/v1/graph/nodes/1` | 500 | Internal server error |
| PUT | `/api/v1/graph/nodes/1` | 500 | Internal server error |
| GET | `/api/v1/graph/paths/46575000000050045/46575000000050045` | 500 | Internal server error |
| GET | `/api/v1/graph/timeline` | 500 | Internal server error |
| GET | `/api/v1/graph/timeline/1` | 500 | Internal server error |
| POST | `/api/v1/officers/` | 500 | Internal server error |
| POST | `/api/v1/stations/` | 500 | Internal server error |
| GET | `/api/v1/storage/download/46575000000050045` | 500 | Internal server error |
| POST | `/api/v1/timeline/` | 500 | Internal server error |
| POST | `/api/v1/vehicles/` | 500 | Internal server error |
| POST | `/api/v1/victims/` | 500 | Internal server error |

## SOFT (sample up to 40)

| Method | Path | Status | Detail |
|--------|------|--------|--------|
| POST | `/api/v1/ai/chat` | 503 |  |
| POST | `/api/v1/analytics/aggregate` | 200 |  |
| GET | `/api/v1/analytics/districts/46575000000050045` | 200 |  |
| DELETE | `/api/v1/bookmarks/` | 422 |  |
| GET | `/api/v1/bookmarks/` | 422 |  |
| GET | `/api/v1/bookmarks/check` | 422 |  |
| GET | `/api/v1/bookmarks/grouped` | 422 |  |
| GET | `/api/v1/copilot/sessions/search` | 404 |  |
| GET | `/api/v1/copilot/sessions/e2e-validate` | 404 |  |
| GET | `/api/v1/copilot/sessions/e2e-validate/export` | 404 |  |
| GET | `/api/v1/criminals/high-risk` | 422 |  |
| POST | `/api/v1/graph/edges` | 422 |  |
| POST | `/api/v1/graph/nodes` | 422 |  |
| POST | `/api/v1/proactive/explain/alert/46575000000050045` | 200 |  |
| POST | `/api/v1/proactive/explain/event/46575000000051058` | 200 |  |
| POST | `/api/v1/proactive/explain/evidence-link/46575000000050045` | 200 |  |
| POST | `/api/v1/proactive/explain/recommendation/46575000000050045` | 200 |  |
| POST | `/api/v1/recommendations/46575000000050045/feedback` | 200 |  |
| GET | `/api/v1/reports/download/seed_attachment.txt` | 404 |  |
| GET | `/api/v1/reports/export/evidence/46575000000051001` | 200 |  |
| GET | `/api/v1/reports/export/investigation/46575000000051001` | 200 |  |
| GET | `/api/v1/reports/export/timeline/46575000000051001` | 200 |  |
| GET | `/api/v1/search/district/stats/BengaluruUrban` | 200 |  |

## SKIP

- `POST /api/v1/ai/chat/stream` — streaming SSE
- `POST /api/v1/attachments/upload` — multipart upload
- `DELETE /api/v1/attachments/{attachment_id}` — skip destructive seed delete
- `DELETE /api/v1/case-links/{link_id}` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}/accused/{accused_id}` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}/act-sections/{assoc_id}` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}/arrest-surrender/{record_id}` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}/chargesheet/{cs_id}` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}/complainant` — skip destructive seed delete
- `DELETE /api/v1/cases/{case_id}/victims/{victim_id}` — skip destructive seed delete
- `POST /api/v1/copilot/chat/stream` — streaming SSE
- `DELETE /api/v1/crime-types/{crimetype_id}` — skip destructive seed delete
- `DELETE /api/v1/crimes/{crime_id}` — skip destructive seed delete
- `DELETE /api/v1/criminals/{criminal_id}` — skip destructive seed delete
- `DELETE /api/v1/datastore/{table}/{row_id}` — skip destructive seed delete
- `DELETE /api/v1/districts/{district_id}` — skip destructive seed delete
- `DELETE /api/v1/investigations/{investigation_id}` — skip destructive seed delete
- `DELETE /api/v1/locations/{location_id}` — skip destructive seed delete
- `DELETE /api/v1/notes/{note_id}` — skip destructive seed delete
- `DELETE /api/v1/officers/{officer_id}` — skip destructive seed delete
- `DELETE /api/v1/persons/{person_id}` — skip destructive seed delete
- `DELETE /api/v1/stations/{station_id}` — skip destructive seed delete
- `POST /api/v1/storage/upload` — multipart upload
- `DELETE /api/v1/timeline/{event_id}` — skip destructive seed delete
- `POST /api/v1/uploads` — multipart upload
- `DELETE /api/v1/vehicles/{vehicle_id}` — skip destructive seed delete
- `DELETE /api/v1/witnesses/{witness_id}` — skip destructive seed delete

## PASS summary by prefix

| Prefix | PASS count |
|--------|------------|
| `api/v1/analytics` | 13 |
| `api/v1/analytics-dashboard` | 6 |
| `api/v1/attachments` | 1 |
| `api/v1/audit` | 18 |
| `api/v1/behavior` | 5 |
| `api/v1/bookmarks` | 5 |
| `api/v1/case-links` | 2 |
| `api/v1/case-status` | 2 |
| `api/v1/cases` | 23 |
| `api/v1/config` | 1 |
| `api/v1/copilot` | 10 |
| `api/v1/crime-types` | 2 |
| `api/v1/crimes` | 5 |
| `api/v1/criminal-timeline` | 4 |
| `api/v1/criminals` | 4 |
| `api/v1/cross-district` | 4 |
| `api/v1/datastore` | 3 |
| `api/v1/districts` | 2 |
| `api/v1/early-warning` | 8 |
| `api/v1/embeddings` | 4 |
| `api/v1/evaluation` | 9 |
| `api/v1/evidence-linking` | 4 |
| `api/v1/fir-intelligence` | 4 |
| `api/v1/graph` | 9 |
| `api/v1/health` | 1 |
| `api/v1/hotspots` | 8 |
| `api/v1/intelligence` | 3 |
| `api/v1/intelligence-timeline` | 7 |
| `api/v1/investigations` | 8 |
| `api/v1/locations` | 3 |
| `api/v1/lookups` | 20 |
| `api/v1/maps` | 7 |
| `api/v1/memory` | 8 |
| `api/v1/metadata` | 1 |
| `api/v1/mo` | 7 |
| `api/v1/monitoring` | 12 |
| `api/v1/notes` | 2 |
| `api/v1/notifications` | 14 |
| `api/v1/officers` | 3 |
| `api/v1/patterns` | 7 |
| `api/v1/persons` | 5 |
| `api/v1/phones` | 5 |
| `api/v1/predictions` | 15 |
| `api/v1/priorities` | 8 |
| `api/v1/proactive` | 10 |
| `api/v1/recommendations` | 7 |
| `api/v1/repeat-offenders` | 5 |
| `api/v1/reports` | 10 |
| `api/v1/search` | 16 |
| `api/v1/similar-cases` | 4 |
| `api/v1/stations` | 2 |
| `api/v1/statistics` | 1 |
| `api/v1/status` | 1 |
| `api/v1/storage` | 3 |
| `api/v1/suspect-risk` | 8 |
| `api/v1/suspects` | 2 |
| `api/v1/timeline` | 1 |
| `api/v1/trends` | 11 |
| `api/v1/uploads` | 1 |
| `api/v1/vehicles` | 3 |
| `api/v1/version` | 1 |
| `api/v1/victims` | 3 |
| `api/v1/witnesses` | 3 |

Full JSON: `ENDPOINT_VALIDATION_20260726T101109Z.json`
