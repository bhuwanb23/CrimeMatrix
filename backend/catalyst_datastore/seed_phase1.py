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

# Load backend/.env so CATALYST_* credentials are available
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(_BACKEND_ROOT, ".env"))
except ImportError:
    pass

from app.db.providers import get_data_provider, get_db_provider_name, init_data_provider
from app.db.providers.catalyst_env import cm_getenv
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
    # NOTE: live table has states.code as bigint (manual create mismatch). Store
    # numeric legacy_id in `code` and keep string codes only in id_map keys.
    for i, (sname, code) in enumerate(STATE_ROWS, start=1):
        row = await _upsert(
            provider,
            "states",
            "legacy_id",
            i,
            {"legacy_id": i, "name": sname, "code": i, "active": True},
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

    # firs / cases — one per CRIME (mirrors SQLite seed/cases.py + seed/firs.py)
    from seed.data import STATIONS as STATION_ROWS

    def _station_name(district_idx: int) -> str:
        dcode = DISTRICTS[district_idx][1]
        for name, _code, district_code in STATION_ROWS:
            if district_code == dcode:
                return name
        return "Cubbon Park PS"

    fir_ids = []
    case_ids = []
    for i, row in enumerate(CRIMES, start=1):
        crime_type_name = CRIME_TYPES[row["type_idx"]][0]
        district_name = DISTRICTS[row["district_idx"]][0]
        fir_number = f"FIR/{i:04d}/2026"
        fir = await _upsert(
            provider,
            "firs",
            "fir_number",
            fir_number,
            {
                "legacy_id": i,
                "title": row["title"],
                "description": row.get("desc") or "",
                "crime_type": crime_type_name,
                "district": district_name,
                "station": _station_name(row["district_idx"]),
                "status": "open" if row.get("status") != "closed" else "closed",
                "complainant_name": f"Complainant {i}",
            },
        )
        fir_ids.append(fir["id"])
        counts["firs"] += 1

        case_status = "closed" if row.get("status") == "closed" else ("active" if row.get("status") == "active" else "open")
        case = await _upsert(
            provider,
            "cases",
            "case_number",
            f"CR/{i:04d}/2026",
            {
                "legacy_id": i,
                "title": row["title"],
                "description": row.get("desc") or "",
                "crime_type": crime_type_name,
                "district": district_name,
                "status": case_status,
                "priority_level": row.get("priority", "medium"),
                "fir_id": fir["id"],
                "latitude": 12.97 + (i * 0.01) % 1,
                "longitude": 77.59 + (i * 0.01) % 1,
            },
        )
        case_ids.append(case["id"])
        counts["cases"] += 1

    # crimes from seed data
    now = datetime.now(timezone.utc)
    base = now - timedelta(days=27)
    for i, row in enumerate(CRIMES):
        type_id = id_map["crime_types_idx"].get(row["type_idx"])
        district_id = id_map["districts_idx"].get(row["district_idx"])
        loc_id = None
        if row.get("location_idx") is not None:
            loc_id = id_map["locations_idx"].get(row["location_idx"])
        occurred = base + timedelta(days=i % 28, hours=10)
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
                "priority_level": row.get("priority", "medium"),
                "occurred_at": occurred.isoformat(),
            },
        )
        id_map.setdefault("crimes", {})[i + 1] = created["id"]
        counts["crimes"] += 1

    # persons / criminals / suspects — denser set for risk / graph pages
    from seed.data import PERSONS, SUSPECTS

    for i, person_row in enumerate(PERSONS, start=1):
        aadhar = f"99990000{i:04d}"
        person = await _upsert(
            provider,
            "persons",
            "aadhar_number",
            aadhar,
            {
                "legacy_id": i,
                "first_name": person_row["first_name"],
                "last_name": person_row["last_name"],
                "district": person_row.get("district", "Bengaluru Urban"),
                "gender": "M" if person_row.get("gender") == "Male" else "F",
            },
        )
        id_map.setdefault("persons", {})[i] = person["id"]
        await _upsert(
            provider,
            "criminals",
            "legacy_id",
            i,
            {
                "person_id": person["id"],
                "alias": person_row["first_name"],
                "risk_score": min(0.95, 0.25 + (i * 0.03)),
                "status": "active",
                "mo_description": "Seed MO",
            },
        )
        counts["persons"] += 1
        counts["criminals"] += 1

    for i, suspect_row in enumerate(SUSPECTS, start=1):
        await _upsert(
            provider,
            "suspects",
            "legacy_id",
            i,
            {
                "name": suspect_row["name"],
                "age": suspect_row.get("age", 30),
                "district": suspect_row.get("district", "Bengaluru Urban"),
                "status": suspect_row.get("status", "open"),
                "risk_score": float(suspect_row.get("risk_score") or 50) / 100.0,
            },
        )
        counts["suspects"] += 1

    # parties / evidence on first 25 cases
    for i, cid in enumerate(case_ids[:25], start=1):
        await _upsert(
            provider,
            "complainants",
            "legacy_id",
            i,
            {"case_id": cid, "name": f"Complainant {i}", "age_year": 25 + (i % 40)},
        )
        await _upsert(
            provider,
            "victims",
            "legacy_id",
            i,
            {"case_id": cid, "name": f"Victim {i}", "age_year": 20 + (i % 45)},
        )
        await _upsert(
            provider,
            "accused",
            "legacy_id",
            i,
            {"case_id": cid, "name": f"Accused {i}", "age_year": 22 + (i % 35)},
        )
        await _upsert(
            provider,
            "evidence",
            "legacy_id",
            i,
            {
                "case_id": cid,
                "evidence_type": "document" if i % 2 else "photo",
                "description": f"Seed evidence for case {i}",
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

    # investigations + notes/timeline — first 40 cases
    inv_ids = []
    for i, case_id in enumerate(case_ids[:40], start=1):
        row = CRIMES[i - 1]
        inv_payload = {
            "case_id": case_id,
            "title": f"Investigation — {row['title'][:80]}",
            "description": row.get("desc") or "Seed investigation",
            "status": "saved" if row.get("status") == "closed" else "active",
            "priority_level": row.get("priority", "medium"),
            "progress": min(90, 10 + i * 2),
            "district": DISTRICTS[row["district_idx"]][0],
        }
        try:
            inv = await _upsert(provider, "investigations", "legacy_id", i, inv_payload)
        except Exception:
            inv_payload.pop("district", None)
            inv = await _upsert(provider, "investigations", "legacy_id", i, inv_payload)
        inv_ids.append(inv["id"])
        await _upsert(
            provider,
            "notes",
            "legacy_id",
            i,
            {"investigation_id": inv["id"], "content": f"Initial case note for investigation {i}"},
        )
        await _upsert(
            provider,
            "timeline_events",
            "legacy_id",
            i,
            {
                "investigation_id": inv["id"],
                "title": f"FIR Registered — INV-{i}",
                "event_type": "fir_filed",
                "event_date": now.isoformat(),
                "description": "Seeded timeline event",
            },
        )
        counts["investigations"] += 1
        counts["notes"] += 1
        counts["timeline_events"] += 1

    # witnesses / case_links / case_status_logs / attachments
    if case_ids and inv_ids:
        await _upsert(
            provider,
            "witnesses",
            "legacy_id",
            1,
            {
                "case_id": case_ids[0],
                "person_id": id_map.get("persons", {}).get(1),
                "statement": "Saw two suspects on a scooter near MG Road.",
                "reliability": "high",
            },
        )
        counts["witnesses"] += 1

        await _upsert(
            provider,
            "case_links",
            "legacy_id",
            1,
            {
                "investigation_id": inv_ids[0],
                "linked_case_id": case_ids[min(1, len(case_ids) - 1)],
                "link_type": "related",
                "description": "Same MO / area",
            },
        )
        counts["case_links"] += 1

        await _upsert(
            provider,
            "case_status_logs",
            "legacy_id",
            1,
            {
                "investigation_id": inv_ids[0],
                "old_status": "open",
                "new_status": "active",
                "notes": "Investigation started",
                "changed_at": now.isoformat(),
            },
        )
        counts["case_status_logs"] += 1

        # attachments metadata (+ optional File Store upload)
        file_path = "seed/readme.txt"
        file_id = None
        folder_id = cm_getenv("CM_FILE_FOLDER_ID")
        if get_db_provider_name() == "catalyst" and folder_id:
            try:
                from app.db.providers.catalyst_client import CatalystClient

                client = CatalystClient()
                meta = client.upload_file(
                    folder_id,
                    "seed_attachment.txt",
                    b"CrimeMatrix Phase 1 seed attachment\n",
                )
                file_id = str(meta.get("id") or meta.get("file_id") or "")
                file_path = f"catalyst://{folder_id}/{file_id}/seed_attachment.txt"
                client.close()
            except Exception as e:
                print(f"  [attachments] File Store upload skipped: {e}")

        await _upsert(
            provider,
            "attachments",
            "legacy_id",
            1,
            {
                "investigation_id": inv_ids[0],
                "filename": "seed_attachment.txt",
                "file_path": file_path,
                "file_id": file_id,
                "folder_id": folder_id,
                "file_size": 40,
                "file_type": "text/plain",
            },
        )
        counts["attachments"] += 1

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
