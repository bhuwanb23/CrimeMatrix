import aiosqlite
import json
from typing import Any, Dict, List, Optional
from storage.base import DBProvider
import structlog

logger = structlog.get_logger()


class SQLiteProvider(DBProvider):
    def __init__(self, db_path: str = "data/ai_memory.db"):
        self.db_path = db_path
        self._db = None

    async def connect(self):
        import os
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else ".", exist_ok=True)
        self._db = await aiosqlite.connect(self.db_path)
        self._db.row_factory = aiosqlite.Row
        await self._db.execute("PRAGMA journal_mode=WAL")
        await self._db.execute("PRAGMA foreign_keys=ON")
        logger.info("sqlite_connected", path=self.db_path)

    async def disconnect(self):
        if self._db:
            await self._db.close()
            logger.info("sqlite_disconnected")

    async def create_table(self, table_name: str, schema: Dict[str, str]):
        columns = ", ".join(f"{col} {dtype}" for col, dtype in schema.items())
        await self._db.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
        await self._db.commit()

    async def insert(self, table: str, data: Dict) -> Any:
        keys = list(data.keys())
        placeholders = ", ".join("?" * len(keys))
        sql = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({placeholders})"
        cursor = await self._db.execute(sql, list(data.values()))
        await self._db.commit()
        return cursor.lastrowid

    async def get(self, table: str, record_id: Any) -> Optional[Dict]:
        cursor = await self._db.execute(f"SELECT * FROM {table} WHERE id = ?", (record_id,))
        row = await cursor.fetchone()
        if row:
            return dict(row)
        return None

    async def query(self, table: str, filters: Dict = None, limit: int = 100, offset: int = 0) -> List[Dict]:
        sql = f"SELECT * FROM {table}"
        params = []
        if filters:
            conditions = []
            for k, v in filters.items():
                if isinstance(v, dict) and "$like" in v:
                    conditions.append(f"{k} LIKE ?")
                    params.append(v["$like"])
                elif isinstance(v, dict) and "$gt" in v:
                    conditions.append(f"{k} > ?")
                    params.append(v["$gt"])
                elif isinstance(v, dict) and "$lt" in v:
                    conditions.append(f"{k} < ?")
                    params.append(v["$lt"])
                else:
                    conditions.append(f"{k} = ?")
                    params.append(v)
            sql += " WHERE " + " AND ".join(conditions)
        sql += f" LIMIT {limit} OFFSET {offset}"
        cursor = await self._db.execute(sql, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def update(self, table: str, record_id: Any, data: Dict) -> bool:
        sets = ", ".join(f"{k} = ?" for k in data.keys())
        sql = f"UPDATE {table} SET {sets} WHERE id = ?"
        cursor = await self._db.execute(sql, list(data.values()) + [record_id])
        await self._db.commit()
        return cursor.rowcount > 0

    async def delete(self, table: str, record_id: Any) -> bool:
        cursor = await self._db.execute(f"DELETE FROM {table} WHERE id = ?", (record_id,))
        await self._db.commit()
        return cursor.rowcount > 0

    async def count(self, table: str, filters: Dict = None) -> int:
        sql = f"SELECT COUNT(*) FROM {table}"
        params = []
        if filters:
            conditions = []
            for k, v in filters.items():
                conditions.append(f"{k} = ?")
                params.append(v)
            sql += " WHERE " + " AND ".join(conditions)
        cursor = await self._db.execute(sql, params)
        row = await cursor.fetchone()
        return row[0] if row else 0

    async def execute(self, sql: str, params: tuple = ()) -> List[Dict]:
        cursor = await self._db.execute(sql, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
