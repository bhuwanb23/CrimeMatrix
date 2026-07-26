#!/usr/bin/env python3
"""Create Phase 1 Data Store tables + File Store folder in Catalyst.

Official Catalyst docs create tables via console. This script:
1. Tries REST create_table / create_column when OAuth credentials are set
2. Writes a console checklist JSON for manual creation
3. Ensures File Store folder `cm_uploads`

Usage:
  set CATALYST_CLIENT_ID=...
  set CATALYST_CLIENT_SECRET=...
  set CATALYST_REFRESH_TOKEN=...
  python -m catalyst_datastore.create_tables
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

from app.db.providers.catalyst_client import CatalystClient, CatalystConfigError
from catalyst_datastore.schema.phase1_tables import (
    FILE_STORE_FOLDER,
    PHASE1_TABLES,
    SEED_ORDER,
    export_schema_json,
)


def write_checklist(out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    checklist = {
        "instructions": [
            "Open Catalyst Console (IN) → Project-Rainfall → Cloud Scale → Data Store",
            "For each table: Create a new Table (alphanumeric + underscore only)",
            "Add columns from schema (skip ROWID/CREATORID/CREATEDTIME/MODIFIEDTIME — automatic)",
            "Then Cloud Scale → File Store → create folder cm_uploads",
            "Set CATALYST_FILE_FOLDER_ID to the folder id after creation",
        ],
        "file_store_folder": FILE_STORE_FOLDER,
        "tables": SEED_ORDER,
        "schema": export_schema_json()["tables"],
    }
    path = out_dir / "CREATE_TABLES_CHECKLIST.json"
    path.write_text(json.dumps(checklist, indent=2), encoding="utf-8")
    return path


def create_via_api(client: CatalystClient, *, skip_existing: bool = True) -> dict:
    existing = {t.get("table_name") or t.get("name") for t in (client.list_tables() or [])}
    created, columns_added, errors = [], [], []

    for table in SEED_ORDER:
        try:
            if table not in existing:
                client.create_table(table)
                created.append(table)
                existing.add(table)
            elif not skip_existing:
                created.append(f"{table}(exists)")

            # columns
            try:
                current = {
                    c.get("column_name")
                    for c in (client.list_columns(table) or [])
                }
            except Exception:
                current = set()
            for col in PHASE1_TABLES[table]:
                name = col["column_name"]
                if name in current:
                    continue
                try:
                    client.create_column(table, col)
                    columns_added.append(f"{table}.{name}")
                except Exception as e:
                    errors.append(f"column {table}.{name}: {e}")
        except Exception as e:
            errors.append(f"table {table}: {e}")

    folder_id = None
    try:
        folders = client.list_folders() or []
        for f in folders:
            if (f.get("folder_name") or f.get("name")) == FILE_STORE_FOLDER:
                folder_id = f.get("id") or f.get("folder_id")
                break
        if not folder_id:
            created_folder = client.create_folder(FILE_STORE_FOLDER)
            folder_id = created_folder.get("id") or created_folder.get("folder_id")
    except Exception as e:
        errors.append(f"file_store: {e}")

    return {
        "tables_created": created,
        "columns_added": columns_added,
        "folder_id": folder_id,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checklist-only",
        action="store_true",
        help="Only write console checklist JSON",
    )
    args = parser.parse_args()

    out = Path(_BACKEND_ROOT) / "catalyst_datastore" / "schema"
    checklist_path = write_checklist(out)
    print(f"Checklist written: {checklist_path}")

    if args.checklist_only:
        return 0

    client = CatalystClient()
    if not client.configured():
        print(
            "No OAuth credentials — checklist ready for console creation.\n"
            "Set CATALYST_CLIENT_ID / CATALYST_CLIENT_SECRET / CATALYST_REFRESH_TOKEN "
            "to create tables via API."
        )
        return 0

    try:
        result = create_via_api(client)
    except CatalystConfigError as e:
        print(f"Config error: {e}")
        return 1
    finally:
        client.close()

    print(json.dumps(result, indent=2))
    if result.get("folder_id"):
        print(f"Set CATALYST_FILE_FOLDER_ID={result['folder_id']}")
    return 0 if not result.get("errors") else 2


if __name__ == "__main__":
    raise SystemExit(main())
