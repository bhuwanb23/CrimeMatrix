# Catalyst Data Store — Phase 1 DB Plan

## What this is

Phase 1 moves **core investigation data** (35 tables) to Zoho Catalyst **Data Store**, with **File Store** for uploads. ML/intel tables stay deferred.

Schema source of truth:

- [`backend/catalyst_datastore/schema/phase1_tables.py`](../backend/catalyst_datastore/schema/phase1_tables.py)
- [`backend/catalyst_datastore/schema/phase1_tables.json`](../backend/catalyst_datastore/schema/phase1_tables.json)

## Environment

| Variable | Purpose |
|----------|---------|
| `DB_PROVIDER` | `sqlite` (default app), `catalyst_local` (local Phase-1 mirror), `catalyst` (live Data Store) |
| `CATALYST_PROJECT_ID` | default `46575000000013023` (Project-Rainfall) |
| `CATALYST_ORG_ID` | default `60079208195` |
| `CATALYST_ENVIRONMENT` | `Development` |
| `CATALYST_API_DOMAIN` | `https://api.catalyst.zoho.in` |
| `CATALYST_ACCOUNTS_DOMAIN` | `https://accounts.zoho.in` |
| `CATALYST_CLIENT_ID` / `CATALYST_CLIENT_SECRET` / `CATALYST_REFRESH_TOKEN` | Self-client OAuth for live Data Store |
| `CATALYST_ACCESS_TOKEN` | Optional short-lived token instead of refresh flow |
| `CATALYST_FILE_FOLDER` | default `cm_uploads` |
| `CATALYST_FILE_FOLDER_ID` | File Store folder id after creation |
| `STORAGE_PROVIDER` | `catalyst` to force File Store uploads |

Register a **Self Client** in Zoho API Console ([api-console.zoho.in](https://api-console.zoho.in/)) and generate a code with these **exact** scopes (comma-separated, no spaces; there is no `tables.ALL` / `files.ALL`):

```text
ZohoCatalyst.projects.ALL,ZohoCatalyst.tables.READ,ZohoCatalyst.tables.columns.READ,ZohoCatalyst.tables.rows.READ,ZohoCatalyst.tables.rows.CREATE,ZohoCatalyst.tables.rows.UPDATE,ZohoCatalyst.tables.rows.DELETE,ZohoCatalyst.folders.ALL,ZohoCatalyst.files.CREATE,ZohoCatalyst.files.READ,ZohoCatalyst.files.DELETE,ZohoCatalyst.zcql.CREATE
```

Exchange the grant code for a refresh token, and put it in `backend/.env` (never commit).

## Create tables (Project-Rainfall)

Catalyst does not officially support creating tables via public REST — console is the supported path.

1. Generate checklist:

```bash
cd backend
python -m catalyst_datastore.create_tables --checklist-only
```

2. Open [Catalyst Console (IN)](https://console.catalyst.zoho.in/) → **Project-Rainfall** → **Cloud Scale → Data Store**.
3. Create each table in `SEED_ORDER` from the checklist JSON; add columns from the schema (skip system `ROWID` / `CREATORID` / `CREATEDTIME` / `MODIFIEDTIME`).
4. **Cloud Scale → File Store** → create folder `cm_uploads`; copy folder id to `CATALYST_FILE_FOLDER_ID`.
5. If your org allows API create, with OAuth set:

```bash
python -m catalyst_datastore.create_tables
```

## Seed

```bash
# Local mirror (no OAuth)
python -m catalyst_datastore.seed_phase1 --provider catalyst_local

# Live Data Store
set DB_PROVIDER=catalyst
python -m catalyst_datastore.seed_phase1 --provider catalyst
```

## Smoke test

```bash
python -m catalyst_datastore.smoke_test --provider catalyst_local
python -m catalyst_datastore.smoke_test --provider catalyst
```

## Backend routes when `DB_PROVIDER=catalyst|catalyst_local`

- `GET /api/v1/districts`, `/crimes`, `/cases`, `/investigations` (list + get)
- `GET/POST /api/v1/datastore/...` ops surface for Phase 1 tables
- Attachments upload uses File Store when `STORAGE_PROVIDER=catalyst` or `DB_PROVIDER=catalyst`

## Constraints

- ZCQL `SELECT`: max **20 columns**, **300 rows** → list endpoints use `LIST_PROJECTIONS` + paging
- Text max **10,000** chars
- **varchar max_length ≤ 255** (longer fields use `text`)
- **`priority` is a reserved keyword** → column is `priority_level`; API still returns `priority`
- API `id` maps from Catalyst `ROWID`; `legacy_id` keeps original SQLite ids for seed remaps

## Auth

Out of scope for Phase 1 (no Catalyst Authentication / API Gateway).
