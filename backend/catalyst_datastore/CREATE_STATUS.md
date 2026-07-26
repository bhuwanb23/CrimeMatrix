# Phase 1 Data Store creation status

**Project:** Project-Rainfall (`46575000000013023`)  
**Org:** `60079208195`  
**Environment:** Development

## Completed in repo

| Deliverable | Location |
|-------------|----------|
| Table/column schema (35 tables) | `backend/catalyst_datastore/schema/phase1_tables.py` + `.json` |
| Console checklist | `backend/catalyst_datastore/schema/CREATE_TABLES_CHECKLIST.json` |
| Create script (OAuth API best-effort) | `python -m catalyst_datastore.create_tables` |
| Local Phase-1 mirror (seeded + smoked) | `DB_PROVIDER=catalyst_local` → `data/catalyst_phase1.db` |
| File Store folder name | `cm_uploads` |

## Live Catalyst console

Table creation via public REST is not officially supported. Console login is required (or OAuth self-client if your org allows POST `/table`).

**Column rules:** do not use reserved name `priority` (use `priority_level`); varchar max length ≤ 255 (longer → `text`).

1. Open https://console.catalyst.zoho.in/ → Project-Rainfall → Cloud Scale → Data Store  
2. Create tables/columns from `CREATE_TABLES_CHECKLIST.json`  
3. File Store → create folder `cm_uploads` → set `CATALYST_FILE_FOLDER_ID`  
4. Add Self Client OAuth vars to `backend/.env`  
5. Run:

```bash
python -m catalyst_datastore.create_tables
python -m catalyst_datastore.seed_phase1 --provider catalyst
python -m catalyst_datastore.smoke_test --provider catalyst
```

## Local verification (done)

```
python -m catalyst_datastore.seed_phase1 --provider catalyst_local
python -m catalyst_datastore.smoke_test --provider catalyst_local
# PASS districts/crimes/cases/investigations
```
