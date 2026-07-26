"""Helpers for Phase 1 Data Store-backed routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from app.db.providers import get_data_provider, get_db_provider_name
from app.db.providers.row_mapper import api_to_store, store_to_api


def using_phase1_store() -> bool:
    return get_db_provider_name() in {"catalyst", "catalyst_local"}


def _normalize_out(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if not row:
        return None
    return store_to_api(row)


def _normalize_in(row: dict[str, Any]) -> dict[str, Any]:
    return api_to_store(row)


async def store_list(
    table: str,
    page: int = 1,
    page_size: int = 20,
    where: Optional[dict] = None,
) -> dict[str, Any]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    result = await provider.list(table, page=page, page_size=page_size, where=where)
    total = result.get("total") or 0
    page_size = result.get("page_size") or page_size
    total_pages = (total + page_size - 1) // page_size if page_size else 0
    items = [_normalize_out(i) or i for i in (result.get("items") or [])]
    return {
        "items": items,
        "total": total,
        "page": result.get("page") or page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


async def store_get(table: str, row_id: int | str) -> Optional[dict[str, Any]]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    return _normalize_out(await provider.get(table, row_id))


async def store_create(table: str, row: dict[str, Any]) -> dict[str, Any]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    created = await provider.insert(table, _normalize_in(row))
    return _normalize_out(created) or created


async def store_update(table: str, row_id: int | str, fields: dict[str, Any]) -> dict[str, Any]:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    updated = await provider.update(table, row_id, _normalize_in(fields))
    return _normalize_out(updated) or updated


async def store_delete(table: str, row_id: int | str) -> bool:
    provider = get_data_provider()
    if not provider:
        raise RuntimeError("Phase 1 data provider not configured")
    return await provider.delete(table, row_id)


def now_store_datetime() -> str:
    """Catalyst-friendly datetime without milliseconds."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


async def store_search_title(
    tables: list[str],
    query: str,
    page: int = 1,
    page_size: int = 20,
) -> dict[str, Any]:
    """Simple title/name contains search across Phase 1 tables."""
    q = (query or "").strip().lower()
    results: list[dict[str, Any]] = []
    for table in tables:
        data = await store_list(table, page=1, page_size=100)
        for item in data["items"]:
            hay = " ".join(
                str(item.get(k) or "")
                for k in ("title", "name", "description", "alias", "registration_number", "badge_number")
            ).lower()
            if q and q not in hay:
                continue
            results.append({"entity": table, **item})
    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = results[start:end]
    return {
        "results": page_items,
        "items": page_items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size else 0,
        "query": query,
    }
