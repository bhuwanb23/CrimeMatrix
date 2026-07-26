from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional


class DataProvider(ABC):
    """Minimal table CRUD used by Phase 1 Catalyst-backed routes and seed."""

    @abstractmethod
    async def insert(self, table: str, row: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    async def get(self, table: str, row_id: int | str) -> Optional[dict[str, Any]]:
        ...

    @abstractmethod
    async def update(self, table: str, row_id: int | str, fields: dict[str, Any]) -> dict[str, Any]:
        ...

    @abstractmethod
    async def delete(self, table: str, row_id: int | str) -> bool:
        ...

    @abstractmethod
    async def list(
        self,
        table: str,
        *,
        page: int = 1,
        page_size: int = 20,
        where: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Return {items, total, page, page_size} with API-shaped rows (id from ROWID)."""
        ...

    @abstractmethod
    async def find_by_legacy_id(self, table: str, legacy_id: int) -> Optional[dict[str, Any]]:
        ...
