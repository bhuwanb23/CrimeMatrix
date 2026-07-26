"""SQLite-backed provider that mirrors Catalyst Phase 1 tables for local/dev.

Uses a separate SQLite file (data/catalyst_phase1.db) with ROWID-like `id` PK
and the same column set as Data Store, so seed/smoke can run without OAuth.
"""

from __future__ import annotations

import os
from typing import Any, Optional

import aiosqlite

from app.db.providers.base import DataProvider
from catalyst_datastore.schema.phase1_tables import PHASE1_TABLES, LIST_PROJECTIONS

_TYPE_MAP = {
    "varchar": "TEXT",
    "text": "TEXT",
    "int": "INTEGER",
    "bigint": "INTEGER",
    "double": "REAL",
    "boolean": "INTEGER",
    "datetime": "TEXT",
    "date": "TEXT",
}


class SqliteDataProvider(DataProvider):
    def __init__(self, path: Optional[str] = None):
        self.path = path or os.getenv("CATALYST_LOCAL_DB", "data/catalyst_phase1.db")

    async def _connect(self) -> aiosqlite.Connection:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        db = await aiosqlite.connect(self.path)
        db.row_factory = aiosqlite.Row
        return db

    async def ensure_schema(self) -> None:
        db = await self._connect()
        try:
            for table, cols in PHASE1_TABLES.items():
                parts = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
                for c in cols:
                    sql_t = _TYPE_MAP.get(c["data_type"], "TEXT")
                    parts.append(f'{c["column_name"]} {sql_t}')
                await db.execute(
                    f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(parts)})"
                )
            await db.commit()
        finally:
            await db.close()

    async def insert(self, table: str, row: dict[str, Any]) -> dict[str, Any]:
        data = {k: v for k, v in row.items() if k != "id" and v is not None}
        if not data:
            raise ValueError("empty row")
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        db = await self._connect()
        try:
            cur = await db.execute(
                f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
                tuple(data.values()),
            )
            await db.commit()
            return await self.get(table, cur.lastrowid) or {"id": cur.lastrowid, **data}
        finally:
            await db.close()

    async def get(self, table: str, row_id: int | str) -> Optional[dict[str, Any]]:
        db = await self._connect()
        try:
            cur = await db.execute(f"SELECT * FROM {table} WHERE id = ?", (row_id,))
            row = await cur.fetchone()
            return dict(row) if row else None
        finally:
            await db.close()

    async def update(self, table: str, row_id: int | str, fields: dict[str, Any]) -> dict[str, Any]:
        data = {k: v for k, v in fields.items() if k != "id"}
        if not data:
            return await self.get(table, row_id) or {}
        sets = ", ".join(f"{k} = ?" for k in data)
        db = await self._connect()
        try:
            await db.execute(
                f"UPDATE {table} SET {sets} WHERE id = ?",
                (*data.values(), row_id),
            )
            await db.commit()
            return await self.get(table, row_id) or {}
        finally:
            await db.close()

    async def delete(self, table: str, row_id: int | str) -> bool:
        db = await self._connect()
        try:
            cur = await db.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
            await db.commit()
            return cur.rowcount > 0
        finally:
            await db.close()

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
        proj = LIST_PROJECTIONS.get(table)
        if proj:
            # Replace ROWID with id for sqlite
            select_cols = ["id" if c == "ROWID" else c for c in proj]
            col_sql = ", ".join(select_cols)
        else:
            col_sql = "*"
        clauses = []
        values: list[Any] = []
        if where:
            for k, v in where.items():
                clauses.append(f"{k} = ?")
                values.append(v)
        where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        db = await self._connect()
        try:
            count_cur = await db.execute(f"SELECT COUNT(*) AS c FROM {table}{where_sql}", values)
            total = (await count_cur.fetchone())["c"]
            cur = await db.execute(
                f"SELECT {col_sql} FROM {table}{where_sql} LIMIT ? OFFSET ?",
                (*values, page_size, offset),
            )
            rows = [dict(r) for r in await cur.fetchall()]
            return {"items": rows, "total": total, "page": page, "page_size": page_size}
        finally:
            await db.close()

    async def find_by_legacy_id(self, table: str, legacy_id: int) -> Optional[dict[str, Any]]:
        result = await self.list(table, page=1, page_size=1, where={"legacy_id": legacy_id})
        items = result.get("items") or []
        return items[0] if items else None
