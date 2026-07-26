"""Seed Phase 1 tables into Catalyst Data Store or local mirror.

Usage (from backend/):
  set DB_PROVIDER=catalyst_local
  python -m catalyst_datastore.seed_phase1

  set DB_PROVIDER=catalyst
  set CATALYST_CLIENT_ID=...
  set CATALYST_CLIENT_SECRET=...
  set CATALYST_REFRESH_TOKEN=...
  python -m catalyst_datastore.seed_phase1
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

from app.db.providers import get_data_provider, get_db_provider_name, init_data_provider
from catalyst_datastore.schema.phase1_tables import SEED_ORDER


async def _upsert(provider, table: str, unique_field: str, unique_value: Any, row: dict) -> dict:
    existing = await provider.list(table, page=1, page_size=5, where={unique_field: unique_value})
    items = existing.get("items") or []
    if items:
        return items[0]
    row = {**row, unique_field: unique_value}
    return await provider.insert(table, row)


async def seed_all() -> dict[str, int]:
    from seed.data import (
        CRIME_TYPES,
        CRIMES,
        DISTRICTS,
        LOCATIONS,
    )
    from seed.states import ROWS as STATE_ROWS

    name = get_db_provider_name()
    if name not in {"catalyst", "catalyst_local"}:
        os.environ["DB_PROVIDER"] = "catalyst_local"
        # clear cached provider
        from app.db.providers import get_data_provider as gdp

        gdp.cache_clear()

    provider = await init_data_provider()
    assert provider is not None

    counts: dict[str, int] = {t: 0 for t in SEED_ORDER}
    id_map: dict[str, dict[Any, Any]] = {}

    # states
    for i, (sname, code) in enumerate(STATE_ROWS, start=1):
        row = await _upsert(
            provider,
            "states",
            "code",
            code,
            {"legacy_id": i, "name": sname, "active": True},
        )
        id_map.setdefault("states", {})[code] = row["id"]
        id_map.setdefault("states_legacy", {})[i] = row["id"]
        counts["states"] += 1

    ka_id = id_map["states"].get("KA")

    # genders / ranks / designations / unit_types / crime_heads / categories / status
    simple_lookups = [
        ("genders", [("Male", "M"), ("Female", "F"), ("Other", "O")], False),
        ("ranks", [("Inspector", "INSP"), ("SI", "SI"), ("Constable", "PC")], True),
        ("designations", [("IO", "IO"), ("SHO", "SHO")], True),
        ("unit_types", [("Police Station", "PS"), ("Circle", "CIR")], True),
        ("case_categories", [("Cognizable", "COG"), ("Non-Cognizable", "NCOG")], True),
        ("case_status_master", [("Open", "OPEN"), ("Closed", "CLOSED"), ("Under Investigation", "UI")], False),
        ("crime_heads", [("Property", "PROP"), ("Person", "PERS"), ("Cyber", "CYBER")], True),
    ]
    for table, rows, with_active in simple_lookups:
        for i, (n, c) in enumerate(rows, start=1):
            payload = {"legacy_id": i, "name": n}
            if with_active:
                payload["active"] = True
            row = await _upsert(provider, table, "code", c, payload)
            id_map.setdefault(table, {})[c] = row["id"]
            counts[table] += 1

    for i, row in enumerate(CRIME_TYPES, start=1):
        n, c = row[0], row[1]
        severity = row[2] if len(row) > 2 else 1
        row_db = await _upsert(
            provider,
            "crime_types",
            "code",
            c,
            {"legacy_id": i, "name": n, "severity_level": severity, "is_active": 1},
        )
        id_map.setdefault("crime_types", {})[c] = row_db["id"]
        id_map.setdefault("crime_types_idx", {})[i - 1] = row_db["id"]
        counts["crime_types"] += 1

    # districts
    for i, (dname, code) in enumerate(DISTRICTS, start=1):
        row = await _upsert(
            provider,
            "districts",
            "code",
            code,
            {
                "legacy_id": i,
                "name": dname,
                "state": "Karnataka",
                "state_id": ka_id,
                "active": True,
            },
        )
        id_map.setdefault("districts", {})[code] = row["id"]
        id_map.setdefault("districts_idx", {})[i - 1] = row["id"]
        counts["districts"] += 1

    # locations: (name, address, lat, lng, district_code, type)
    for i, loc in enumerate(LOCATIONS, start=1):
        name_, _addr, lat, lng, d_code, loc_type = loc
        row = await _upsert(
            provider,
            "locations",
            "name",
            name_,
            {
                "legacy_id": i,
                "address": _addr,
                "latitude": lat,
                "longitude": lng,
                "district_id": id_map["districts"].get(d_code),
                "type": loc_type,
            },
        )
        id_map.setdefault("locations_idx", {})[i - 1] = row["id"]
        counts["locations"] += 1

    # stations (minimal)
    first_district = next(iter(id_map["districts"].values()))
    for i, (sname, code) in enumerate(
        [("Cubbon Park PS", "CPS"), ("Whitefield PS", "WPS"), ("Mysuru Central PS", "MPS")],
        start=1,
    ):
        row = await _upsert(
            provider,
            "stations",
            "code",
            code,
            {
                "legacy_id": i,
                "name": sname,
                "district_id": first_district,
                "state_id": ka_id,
                "active": True,
            },
        )
        id_map.setdefault("stations", {})[code] = row["id"]
        counts["stations"] += 1

    # officers
    for i, badge in enumerate(["KGID1001", "KGID1002", "KGID1003"], start=1):
        row = await _upsert(
            provider,
            "officers",
            "badge_number",
            badge,
            {
                "legacy_id": i,
                "first_name": f"Officer{i}",
                "rank": "Inspector",
                "district_id": first_district,
                "station_id": next(iter(id_map["stations"].values())),
                "status": "active",
            },
        )
        id_map.setdefault("officers", {})[i] = row["id"]
        counts["officers"] += 1

    # acts / sections
    act = await _upsert(
        provider,
        "acts",
        "act_code",
        "IPC",
        {"legacy_id": 1, "name": "Indian Penal Code", "short_name": "IPC", "active": True},
    )
    counts["acts"] += 1
    for i, (sname, scode) in enumerate([("Theft", "379"), ("Robbery", "392"), ("Cheating", "420")], start=1):
        await _upsert(
            provider,
            "sections",
            "section_code",
            scode,
            {"legacy_id": i, "name": sname, "act_id": act["id"], "active": True},
        )
        counts["sections"] += 1

    # firs / cases
    fir_ids = []
    for i in range(1, 6):
        fir = await _upsert(
            provider,
            "firs",
            "fir_number",
            f"FIR/BNG/2026/{i:04d}",
            {
                "legacy_id": i,
                "title": f"Sample FIR {i}",
                "description": "Seeded FIR for Catalyst Phase 1",
                "crime_type": "theft",
                "district": "Bengaluru Urban",
                "station": "Cubbon Park PS",
                "status": "open",
                "complainant_name": f"Complainant {i}",
            },
        )
        fir_ids.append(fir["id"])
        counts["firs"] += 1

    case_ids = []
    for i, fir_id in enumerate(fir_ids, start=1):
        case = await _upsert(
            provider,
            "cases",
            "case_number",
            f"CASE/BNG/2026/{i:04d}",
            {
                "legacy_id": i,
                "title": f"Sample Case {i}",
                "description": "Seeded case",
                "crime_type": "theft",
                "district": "Bengaluru Urban",
                "status": "open",
                "priority": "medium",
                "fir_id": fir_id,
                "latitude": 12.97,
                "longitude": 77.59,
            },
        )
        case_ids.append(case["id"])
        counts["cases"] += 1

    # crimes from seed data
    now = datetime.now(timezone.utc)
    base = now - timedelta(days=6)
    for i, row in enumerate(CRIMES):
        type_id = id_map["crime_types_idx"].get(row["type_idx"])
        district_id = id_map["districts_idx"].get(row["district_idx"])
        loc_id = None
        if row.get("location_idx") is not None:
            loc_id = id_map["locations_idx"].get(row["location_idx"])
        occurred = base + timedelta(days=i % 7, hours=10)
        created = await _upsert(
            provider,
            "crimes",
            "title",
            row["title"],
            {
                "legacy_id": i + 1,
                "description": row.get("desc"),
                "crime_type_id": type_id,
                "district_id": district_id,
                "location_id": loc_id,
                "status": row.get("status", "open"),
                "priority": row.get("priority", "medium"),
                "occurred_at": occurred.isoformat(),
            },
        )
        id_map.setdefault("crimes", {})[i + 1] = created["id"]
        counts["crimes"] += 1

    # persons / criminals / suspects
    for i in range(1, 4):
        person = await _upsert(
            provider,
            "persons",
            "aadhar_number",
            f"99990000{i:04d}",
            {
                "legacy_id": i,
                "first_name": f"Person{i}",
                "last_name": "Seed",
                "district": "Bengaluru Urban",
                "gender": "M",
            },
        )
        await _upsert(
            provider,
            "criminals",
            "legacy_id",
            i,
            {
                "person_id": person["id"],
                "alias": f"Alias{i}",
                "risk_score": 0.4 * i,
                "status": "active",
                "mo_description": "Seed MO",
            },
        )
        await _upsert(
            provider,
            "suspects",
            "legacy_id",
            i,
            {
                "name": f"Suspect {i}",
                "age": 25 + i,
                "district": "Bengaluru Urban",
                "status": "open",
                "risk_score": 0.3 * i,
            },
        )
        counts["persons"] += 1
        counts["criminals"] += 1
        counts["suspects"] += 1

    # parties on first case
    if case_ids:
        cid = case_ids[0]
        await _upsert(
            provider,
            "complainants",
            "legacy_id",
            1,
            {"case_id": cid, "name": "Seed Complainant", "age_year": 40},
        )
        await _upsert(
            provider,
            "victims",
            "legacy_id",
            1,
            {"case_id": cid, "name": "Seed Victim", "age_year": 35},
        )
        await _upsert(
            provider,
            "accused",
            "legacy_id",
            1,
            {"case_id": cid, "name": "Seed Accused", "age_year": 28},
        )
        await _upsert(
            provider,
            "evidence",
            "legacy_id",
            1,
            {
                "case_id": cid,
                "evidence_type": "document",
                "description": "Seed evidence",
                "status": "logged",
                "file_path": "",
            },
        )
        counts["complainants"] += 1
        counts["victims"] += 1
        counts["accused"] += 1
        counts["evidence"] += 1

    # vehicles / phones
    await _upsert(
        provider,
        "vehicles",
        "registration_number",
        "KA01AB1234",
        {"legacy_id": 1, "make": "Honda", "model": "Activa", "color": "Black", "status": "active"},
    )
    await _upsert(
        provider,
        "phones",
        "number",
        "9876543210",
        {"legacy_id": 1, "carrier": "Airtel", "type": "mobile", "status": "active"},
    )
    counts["vehicles"] += 1
    counts["phones"] += 1

    # investigations + notes/timeline
    for i, case_id in enumerate(case_ids[:3], start=1):
        inv = await _upsert(
            provider,
            "investigations",
            "legacy_id",
            i,
            {
                "case_id": case_id,
                "title": f"Investigation {i}",
                "description": "Seed investigation",
                "status": "active",
                "priority": "medium",
                "progress": 20 * i,
                "district": "Bengaluru Urban",
            },
        )
        await _upsert(
            provider,
            "notes",
            "legacy_id",
            i,
            {"investigation_id": inv["id"], "content": f"Seed note {i}"},
        )
        await _upsert(
            provider,
            "timeline_events",
            "legacy_id",
            i,
            {
                "investigation_id": inv["id"],
                "title": f"Event {i}",
                "event_type": "update",
                "event_date": now.isoformat(),
                "description": "Seeded timeline event",
            },
        )
        counts["investigations"] += 1
        counts["notes"] += 1
        counts["timeline_events"] += 1

    # crime_sub_heads
    head_id = next(iter(id_map["crime_heads"].values()))
    await _upsert(
        provider,
        "crime_sub_heads",
        "code",
        "PROP_THEFT",
        {"legacy_id": 1, "name": "Theft", "crime_head_id": head_id},
    )
    counts["crime_sub_heads"] += 1

    return {k: v for k, v in counts.items() if v}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--provider",
        choices=["catalyst", "catalyst_local"],
        default=None,
        help="Override DB_PROVIDER",
    )
    args = parser.parse_args()
    if args.provider:
        os.environ["DB_PROVIDER"] = args.provider
        from app.db.providers import get_data_provider

        get_data_provider.cache_clear()

    counts = asyncio.run(seed_all())
    print(f"Seeded provider={get_db_provider_name()}")
    for table, n in counts.items():
        print(f"  {table}: {n}")
    print(f"TOTAL_TABLES_TOUCHED={len(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
