"""Normalize Catalyst rows <-> API shapes (ROWID -> id)."""

from __future__ import annotations

from typing import Any, Optional


def to_api_row(row: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
    if not row:
        return None
    # Catalyst may nest as {TableName: {...}} from ZCQL
    if len(row) == 1:
        only = next(iter(row.values()))
        if isinstance(only, dict) and ("ROWID" in only or "rowid" in only or "legacy_id" in only):
            row = only
    out = dict(row)
    rowid = out.pop("ROWID", None)
    if rowid is None:
        rowid = out.pop("rowid", None)
    if rowid is not None:
        out["id"] = int(rowid) if str(rowid).isdigit() else rowid
    # Drop system columns from API payloads
    for key in ("CREATORID", "CREATEDTIME", "MODIFIEDTIME", "creatorid", "createdtime", "modifiedtime"):
        out.pop(key, None)
    return out


def from_api_row(row: dict[str, Any], *, include_rowid: bool = False) -> dict[str, Any]:
    out = {k: v for k, v in row.items() if v is not None and k not in ("id", "ROWID")}
    if include_rowid and "id" in row:
        out["ROWID"] = row["id"]
    return out


def escape_zcql(value: Any) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value).replace("\\", "\\\\").replace("'", "\\'")
    return f"'{s}'"
