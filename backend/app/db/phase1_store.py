"""Helpers for Phase 1 Data Store-backed routes."""

from __future__ import annotations

from typing import Any, Optional

from app.db.providers import get_data_provider, get_db_provider_name


def using_phase1_store() -> bool:
    return get_db_provider_name() in {"catalyst", "catalyst_local"}


async def store_list(table: str, page: int = 1, page_size: int = 20, where: Optional[dict] = None) -> dict[str, Any]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    result = await provider.list(table, page=page, page_size=page_size, where=where)
    total = result.get("total") or 0
    page_size = result.get("page_size") or page_size
    total_pages = (total + page_size - 1) // page_size if page_size else 0
    return {
        "items": result.get("items") or [],
        "total": total,
        "page": result.get("page") or page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


async def store_get(table: str, row_id: int | str) -> Optional[dict[str, Any]]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    return await provider.get(table, row_id)


async def store_create(table: str, row: dict[str, Any]) -> dict[str, Any]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    return await provider.insert(table, row)


async def store_delete(table: str, row_id: int | str) -> bool:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    return await provider.delete(table, row_id)
