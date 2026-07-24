"""Shared helpers for idempotent seeding."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_one(db: AsyncSession, model, **filters):
    stmt = select(model)
    for key, value in filters.items():
        stmt = stmt.where(getattr(model, key) == value)
    return (await db.execute(stmt)).scalar_one_or_none()


async def ensure(db: AsyncSession, model, *, unique: dict, defaults: dict | None = None):
    """Insert row if no match on unique filters. Returns (instance, created)."""
    existing = await get_one(db, model, **unique)
    if existing:
        return existing, False
    payload = {**unique, **(defaults or {})}
    obj = model(**payload)
    db.add(obj)
    await db.flush()
    return obj, True


async def count_new(created_flags: list[bool]) -> int:
    return sum(1 for c in created_flags if c)
