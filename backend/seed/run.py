"""Ordered seed runner.

Usage (from backend/):
    python -m seed
    python -m seed --fresh
    python -m seed --fresh --bootstrap   # seed then POST detect/batch/build (API must be up)
    python -m seed --bootstrap-only      # intelligence only
    python -m seed --only states,districts,crimes
    python -m seed --list
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys

# Ensure backend root is on path when run as script
_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

# Register all ORM models before create_all
import app.models  # noqa: F401
from app.db.session import async_session, init_db

# (table_key, module)
SEED_STEPS = [
    ("states", "seed.states"),
    ("unit_types", "seed.unit_types"),
    ("ranks", "seed.ranks"),
    ("designations", "seed.designations"),
    ("blood_groups", "seed.blood_groups"),
    ("genders", "seed.genders"),
    ("religions", "seed.religions"),
    ("occupations", "seed.occupations"),
    ("caste_master", "seed.caste_master"),
    ("case_categories", "seed.case_categories"),
    ("gravity_offences", "seed.gravity_offences"),
    ("crime_heads", "seed.crime_heads"),
    ("crime_sub_heads", "seed.crime_sub_heads"),
    ("case_status_master", "seed.case_status_master"),
    ("acts", "seed.acts"),
    ("sections", "seed.sections"),
    ("arrest_surrender_types", "seed.arrest_surrender_types"),
    ("districts", "seed.districts"),
    ("courts", "seed.courts"),
    ("stations", "seed.stations"),
    ("crime_types", "seed.crime_types"),
    ("locations", "seed.locations"),
    ("users", "seed.users"),
    ("officers", "seed.officers"),
    ("crimes", "seed.crimes"),
    ("firs", "seed.firs"),
    ("cases", "seed.cases"),
    ("complainants", "seed.complainants"),
    ("victims", "seed.victims"),
    ("accused", "seed.accused"),
    ("evidence", "seed.evidence"),
    ("persons", "seed.persons"),
    ("criminals", "seed.criminals"),
    ("suspects", "seed.suspects"),
    ("investigations", "seed.investigations"),
    ("notes", "seed.notes"),
    ("timeline_events", "seed.timeline_events"),
    ("bookmarks", "seed.bookmarks"),
    ("case_priorities", "seed.case_priorities"),
    ("alerts", "seed.alerts"),
    ("early_warning_alerts", "seed.early_warning_alerts"),
    ("report_templates", "seed.report_templates"),
    ("reports", "seed.reports"),
    ("crime_hotspots", "seed.crime_hotspots"),
]


def _import_seed(module_path: str):
    import importlib
    mod = importlib.import_module(module_path)
    return mod.seed


def _db_file_path() -> str | None:
    url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///data/crimematrix.db")
    if "sqlite" not in url:
        return None
    # sqlite+aiosqlite:///relative/path or ////absolute
    path = url.split(":///", 1)[-1]
    if not os.path.isabs(path):
        path = os.path.join(_BACKEND_ROOT, path)
    return path


async def run_all(only: set[str] | None = None, fresh: bool = False) -> dict[str, int]:
    os.makedirs(os.path.join(_BACKEND_ROOT, "data"), exist_ok=True)
    if fresh:
        db_path = _db_file_path()
        if db_path and os.path.exists(db_path):
            os.remove(db_path)
            print(f"Removed existing database: {db_path}")
        # Also clear SQLite sidecars if present
        for suffix in ("-wal", "-shm"):
            side = f"{db_path}{suffix}" if db_path else None
            if side and os.path.exists(side):
                os.remove(side)
    await init_db()
    results: dict[str, int] = {}

    async with async_session() as db:
        for key, module_path in SEED_STEPS:
            if only and key not in only:
                continue
            seed_fn = _import_seed(module_path)
            try:
                count = await seed_fn(db)
                await db.commit()
                results[key] = count
                print(f"  [{key}] +{count}")
            except Exception as exc:
                await db.rollback()
                print(f"  [{key}] FAILED: {exc}")
                raise
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed CrimeMatrix database")
    parser.add_argument("--only", help="Comma-separated table keys to seed")
    parser.add_argument("--list", action="store_true", help="List seed steps in order")
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Delete SQLite DB and recreate tables before seeding (recommended once)",
    )
    parser.add_argument(
        "--bootstrap",
        action="store_true",
        help="After seeding (or alone), POST detect/batch/build endpoints (API must be running)",
    )
    parser.add_argument(
        "--bootstrap-only",
        action="store_true",
        help="Skip table seeding; only run intelligence bootstrap",
    )
    args = parser.parse_args(argv)

    if args.list:
        for key, module in SEED_STEPS:
            print(f"{key:24} {module}")
        return 0

    only = None
    if args.only:
        only = {x.strip() for x in args.only.split(",") if x.strip()}
        known = {k for k, _ in SEED_STEPS}
        unknown = only - known
        if unknown:
            print(f"Unknown seed keys: {', '.join(sorted(unknown))}")
            return 1

    if not args.bootstrap_only:
        print("Seeding CrimeMatrix database…")
        results = asyncio.run(run_all(only=only, fresh=args.fresh))
        total = sum(results.values())
        print(f"Done. {total} new rows across {len(results)} tables.")

    if args.bootstrap or args.bootstrap_only:
        print("Bootstrapping intelligence pipelines…")
        from seed.bootstrap_intelligence import run_bootstrap
        boot = asyncio.run(run_bootstrap())
        ok = sum(1 for v in boot.values() if v == "ok")
        print(f"Bootstrap finished: {ok}/{len(boot)} steps OK.")
        if boot.get("_error"):
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
