"""DB provider factory.

DB_PROVIDER:
  - sqlite (default) — existing SQLAlchemy app DB (routes unchanged)
  - catalyst — live Catalyst Data Store (needs OAuth env)
  - catalyst_local — Phase-1 SQLite mirror of Data Store schema (local smoke/seed)
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from app.db.providers.base import DataProvider


def get_db_provider_name() -> str:
    return (os.getenv("DB_PROVIDER") or "sqlite").strip().lower()


@lru_cache(maxsize=1)
def get_data_provider() -> Optional[DataProvider]:
    name = get_db_provider_name()
    if name == "catalyst":
        from app.db.providers.catalyst_provider import CatalystDataProvider

        return CatalystDataProvider()
    if name == "catalyst_local":
        from app.db.providers.sqlite_provider import SqliteDataProvider

        return SqliteDataProvider()
    return None


async def init_data_provider() -> Optional[DataProvider]:
    provider = get_data_provider()
    if provider is None:
        return None
    # Local mirror needs schema bootstrap
    ensure = getattr(provider, "ensure_schema", None)
    if ensure:
        await ensure()
    return provider
