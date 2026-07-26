# Backend endpoint validation

- Base: `https://crimematrix-backend-50044181811.development.catalystappsail.in`
- Generated: `2026-07-26T11:08:33.914748+00:00`
- Total operations: **461**
- PASS: **409**
- SOFT: **24** (empty/validation/missing-id acceptable)
- FAIL: **0**
- SKIP: **28** (destructive/multipart/stream)

## FAIL details

_None_

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
| POST | `/api/v1/datastore/districts` | 422 |  |
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
| GET | `/api/v1/storage/download/46575000000050045` | 404 |  |

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
| `api/v1/analytics` | 15 |
| `api/v1/analytics-dashboard` | 6 |
| `api/v1/attachments` | 1 |
| `api/v1/audit` | 18 |
| `api/v1/behavior` | 5 |
| `api/v1/bookmarks` | 5 |
| `api/v1/case-links` | 2 |
| `api/v1/case-status` | 2 |
| `api/v1/cases` | 24 |
| `api/v1/config` | 1 |
| `api/v1/copilot` | 10 |
| `api/v1/crime-types` | 3 |
| `api/v1/crimes` | 5 |
| `api/v1/criminal-timeline` | 4 |
| `api/v1/criminals` | 5 |
| `api/v1/cross-district` | 5 |
| `api/v1/datastore` | 3 |
| `api/v1/districts` | 3 |
| `api/v1/early-warning` | 8 |
| `api/v1/embeddings` | 4 |
| `api/v1/evaluation` | 9 |
| `api/v1/evidence-linking` | 5 |
| `api/v1/fir-intelligence` | 4 |
| `api/v1/graph` | 21 |
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
| `api/v1/officers` | 4 |
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
| `api/v1/stations` | 3 |
| `api/v1/statistics` | 1 |
| `api/v1/status` | 1 |
| `api/v1/storage` | 3 |
| `api/v1/suspect-risk` | 8 |
| `api/v1/suspects` | 2 |
| `api/v1/timeline` | 2 |
| `api/v1/trends` | 11 |
| `api/v1/uploads` | 1 |
| `api/v1/vehicles` | 4 |
| `api/v1/version` | 1 |
| `api/v1/victims` | 4 |
| `api/v1/witnesses` | 3 |

Full JSON dumps are gitignored (re-run the validator locally if needed).
