"""Direct Phase 1 Data Store CRUD (for smoke tests / ops)."""

from fastapi import APIRouter, HTTPException, Query
from typing import Any, Optional

from app.core.response import success_response
from app.db.phase1_store import store_create, store_delete, store_get, store_list, using_phase1_store
from catalyst_datastore.schema.phase1_tables import PHASE1_TABLES, SEED_ORDER

router = APIRouter()


@router.get("/status")
async def datastore_status():
    from app.db.providers import get_db_provider_name

    return success_response(
        data={
            "provider": get_db_provider_name(),
            "phase1_active": using_phase1_store(),
            "tables": list(SEED_ORDER),
            "table_count": len(PHASE1_TABLES),
        }
    )


@router.get("/{table}")
async def list_table(
    table: str,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=300),
):
    if table not in PHASE1_TABLES:
        return success_response(message=f"Unknown Phase 1 table: {table}")
    if not using_phase1_store():
        return success_response(message="Set DB_PROVIDER=catalyst or catalyst_local")
    data = await store_list(table, page=page, page_size=page_size)
    return success_response(data=data)


@router.get("/{table}/{row_id}")
async def get_table_row(table: str, row_id: int):
    if table not in PHASE1_TABLES:
        return success_response(message=f"Unknown Phase 1 table: {table}")
    if not using_phase1_store():
        return success_response(message="Set DB_PROVIDER=catalyst or catalyst_local")
    row = await store_get(table, row_id)
    if not row:
        return success_response(message="Not found")
    return success_response(data=row)


@router.post("/{table}")
async def create_table_row(table: str, body: dict[str, Any]):
    if table not in PHASE1_TABLES:
        return success_response(message=f"Unknown Phase 1 table: {table}")
    if not using_phase1_store():
        return success_response(message="Set DB_PROVIDER=catalyst or catalyst_local")
    if not body:
        raise HTTPException(status_code=422, detail="Request body cannot be empty")
    try:
        row = await store_create(table, body)
        return success_response(data=row, message="Created")
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e)[:300])


@router.delete("/{table}/{row_id}")
async def delete_table_row(table: str, row_id: int):
    if table not in PHASE1_TABLES:
        return success_response(message=f"Unknown Phase 1 table: {table}")
    if not using_phase1_store():
        return success_response(message="Set DB_PROVIDER=catalyst or catalyst_local")
    ok = await store_delete(table, row_id)
    return success_response(message="Deleted" if ok else "Not found")
