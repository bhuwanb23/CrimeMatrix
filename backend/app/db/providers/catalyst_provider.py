"""Catalyst Data Store provider (Phase 1)."""

from __future__ import annotations

from typing import Any, Optional

from app.db.providers.base import DataProvider
from app.db.providers.catalyst_client import CatalystClient
from app.db.providers.row_mapper import escape_zcql, from_api_row, to_api_row
from catalyst_datastore.schema.phase1_tables import LIST_PROJECTIONS


class CatalystDataProvider(DataProvider):
    def __init__(self, client: Optional[CatalystClient] = None):
        self.client = client or CatalystClient()

    async def insert(self, table: str, row: dict[str, Any]) -> dict[str, Any]:
        payload = from_api_row(row)
        created = self.client.insert_row(table, payload)
        return to_api_row(created) or {}

    async def get(self, table: str, row_id: int | str) -> Optional[dict[str, Any]]:
        try:
            row = self.client.get_row(table, row_id)
            return to_api_row(row)
        except RuntimeError:
            return None

    async def update(self, table: str, row_id: int | str, fields: dict[str, Any]) -> dict[str, Any]:
        payload = from_api_row(fields)
        payload["ROWID"] = row_id
        updated = self.client.update_row(table, payload)
        return to_api_row(updated) or {}

    async def delete(self, table: str, row_id: int | str) -> bool:
        try:
            self.client.delete_row(table, row_id)
            return True
        except RuntimeError:
            return False

    async def list(
        self,
        table: str,
        *,
        page: int = 1,
        page_size: int = 20,
        where: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        page = max(1, page)
        page_size = min(max(1, page_size), 300)
        offset = (page - 1) * page_size
        cols = LIST_PROJECTIONS.get(table) or ["ROWID"]
        col_sql = ", ".join(cols)
        where_sql = ""
        if where:
            parts = [f"{k} = {escape_zcql(v)}" for k, v in where.items()]
            where_sql = " WHERE " + " AND ".join(parts)
        query = (
            f"SELECT {col_sql} FROM {table}{where_sql} "
            f"LIMIT {offset}, {page_size}"
        )
        try:
            raw = self.client.zcql_execute(query)
            items = [to_api_row(r) for r in (raw or [])]
            items = [i for i in items if i]
        except RuntimeError:
            # Fallback: paged rows API (no server-side filter)
            all_rows = self.client.list_all_rows(table, page_size=100, limit=offset + page_size)
            mapped = [to_api_row(r) for r in all_rows]
            mapped = [m for m in mapped if m]
            if where:
                mapped = [
                    m for m in mapped
                    if all(str(m.get(k)) == str(v) for k, v in where.items())
                ]
            items = mapped[offset : offset + page_size]
        return {
            "items": items,
            "total": len(items) if page == 1 and len(items) < page_size else offset + len(items),
            "page": page,
            "page_size": page_size,
        }

    async def find_by_legacy_id(self, table: str, legacy_id: int) -> Optional[dict[str, Any]]:
        result = await self.list(table, page=1, page_size=1, where={"legacy_id": legacy_id})
        items = result.get("items") or []
        return items[0] if items else None
