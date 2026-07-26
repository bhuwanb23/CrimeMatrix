#!/usr/bin/env python3
"""Smoke-test Phase 1 Data Store provider.

Default: catalyst_local (no OAuth required).
Live: DB_PROVIDER=catalyst with OAuth env vars.

Usage (from backend/):
  python -m catalyst_datastore.smoke_test
  python -m catalyst_datastore.smoke_test --provider catalyst
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)


async def run(provider_name: str) -> int:
    os.environ["DB_PROVIDER"] = provider_name
    from app.db.providers import get_data_provider, init_data_provider

    get_data_provider.cache_clear()
    provider = await init_data_provider()
    if provider is None:
        print("FAIL: no provider")
        return 1

    results = []

    async def check(label: str, coro):
        try:
            data = await coro
            ok = bool(data)
            results.append((label, ok, data))
            print(f"{'PASS' if ok else 'FAIL'}  {label}")
            return data
        except Exception as e:
            results.append((label, False, str(e)))
            print(f"FAIL  {label}: {e}")
            return None

    # ensure a district exists
    districts = await check("list districts", provider.list("districts", page=1, page_size=5))
    if districts and not districts.get("items"):
        await provider.insert(
            "districts",
            {"legacy_id": 9999, "name": "Smoke District", "code": "SMOKE", "active": True},
        )
        districts = await check("list districts (after insert)", provider.list("districts", page=1, page_size=5))

    items = (districts or {}).get("items") or []
    if items:
        did = items[0]["id"]
        await check("get district", provider.get("districts", did))

    crimes = await check("list crimes", provider.list("crimes", page=1, page_size=5))
    if crimes and not crimes.get("items"):
        await provider.insert(
            "crimes",
            {
                "legacy_id": 9999,
                "title": "Smoke Crime",
                "status": "open",
                "priority": "low",
                "district_id": items[0]["id"] if items else None,
            },
        )
        await check("list crimes (after insert)", provider.list("crimes", page=1, page_size=5))

    cases = await check("list cases", provider.list("cases", page=1, page_size=5))
    if cases and not cases.get("items"):
        await provider.insert(
            "cases",
            {
                "legacy_id": 9999,
                "case_number": "SMOKE/CASE/1",
                "title": "Smoke Case",
                "crime_type": "theft",
                "district": "Smoke District",
                "status": "open",
            },
        )
        await check("list cases (after insert)", provider.list("cases", page=1, page_size=5))

    inv = await check("list investigations", provider.list("investigations", page=1, page_size=5))
    if inv and not inv.get("items"):
        case_items = (await provider.list("cases", page=1, page_size=1)).get("items") or []
        await provider.insert(
            "investigations",
            {
                "legacy_id": 9999,
                "title": "Smoke Investigation",
                "status": "active",
                "case_id": case_items[0]["id"] if case_items else None,
                "district": "Smoke District",
                "progress": 10,
            },
        )
        await check(
            "list investigations (after insert)",
            provider.list("investigations", page=1, page_size=5),
        )

    passed = sum(1 for _, ok, _ in results if ok)
    failed = sum(1 for _, ok, _ in results if not ok)
    print("=" * 48)
    print(f"provider={provider_name} PASS={passed} FAIL={failed}")
    return 0 if failed == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default=os.getenv("DB_PROVIDER", "catalyst_local"))
    args = parser.parse_args()
    return asyncio.run(run(args.provider))


if __name__ == "__main__":
    raise SystemExit(main())
