from datetime import datetime, timedelta, timezone
import random

from seed.data import CRIMES, CRIME_TYPES, DISTRICTS, LOCATIONS
from seed.utils import get_one
from app.models.crime import Crime
from app.models.crimetype import CrimeType
from app.models.district import District
from app.models.location import Location


async def seed(db) -> int:
    n = 0
    # Seed crimes across the last 7 days for trend charts, patterns, forecasts
    now = datetime.now(timezone.utc)
    base = now - timedelta(days=6)

    for i, row in enumerate(CRIMES):
        existing = await get_one(db, Crime, title=row["title"])
        if existing:
            continue

        type_code = CRIME_TYPES[row["type_idx"]][1]
        district_code = DISTRICTS[row["district_idx"]][1]
        crime_type = await get_one(db, CrimeType, code=type_code)
        district = await get_one(db, District, code=district_code)

        location_id = None
        loc_idx = row.get("location_idx")
        if loc_idx is not None and loc_idx < len(LOCATIONS):
            loc = await get_one(db, Location, name=LOCATIONS[loc_idx][0])
            location_id = loc.id if loc else None

        # Spread crimes across 7 days with varied hours for seasonal patterns
        day_offset = i % 7
        hour = random.choice([2, 5, 8, 10, 13, 15, 18, 21])  # varied hours
        occurred = base + timedelta(days=day_offset, hours=hour, minutes=random.randint(0, 59))

        db.add(Crime(
            title=row["title"],
            description=row["desc"],
            crime_type_id=crime_type.id if crime_type else None,
            district_id=district.id if district else None,
            location_id=location_id,
            status=row["status"],
            priority=row["priority"],
            occurred_at=occurred,
        ))
        n += 1

    # Add extra crimes to ensure 7 days of data with 5-7 crimes per day
    extra_crimes = [
        {"title": "Night theft in Koramangala residential area", "desc": "Multiple houses burgled between 2-4 AM. Entry through balcony. Gold and electronics stolen.", "type_idx": 2, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 3},
        {"title": "Chain snatching near Majestic metro", "desc": "Woman's gold chain snatched by two persons on scooter. CCTV footage available.", "type_idx": 12, "district_idx": 0, "status": "active", "priority": "medium", "location_idx": 1},
        {"title": "Mobile theft at Brigade Road", "desc": "iPhone stolen from cafe table. Suspect caught on camera.", "type_idx": 0, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 2},
        {"title": "Robbery at wine shop in Mysuru", "desc": "Armed robbery at late-night wine shop. Two suspects on motorcycle.", "type_idx": 1, "district_idx": 2, "status": "active", "priority": "high", "location_idx": 5},
        {"title": "Burglary at IT company Whitefield", "desc": "Laptops and servers stolen from office. Night guard suspect.", "type_idx": 2, "district_idx": 0, "status": "open", "priority": "high", "location_idx": 4},
        {"title": "Cyber fraud via fake lottery message", "desc": "Multiple victims lost money through fake lottery winnings scam.", "type_idx": 6, "district_idx": 0, "status": "active", "priority": "medium", "location_idx": 0},
        {"title": "Drug peddling near school in Mangaluru", "desc": "Students being targeted by drug dealers near school compound.", "type_idx": 8, "district_idx": 3, "status": "active", "priority": "high", "location_idx": 6},
        {"title": "Vehicle theft from apartment complex", "desc": "Scooter stolen from covered parking. Lock cut.", "type_idx": 11, "district_idx": 0, "status": "open", "priority": "medium", "location_idx": 3},
        {"title": "Assault during road rage incident", "desc": "Driver attacked with rod during traffic dispute.", "type_idx": 4, "district_idx": 0, "status": "active", "priority": "medium", "location_idx": 1},
        {"title": "Cheating via fake investment scheme", "desc": "Multiple investors lost money in Ponzi scheme.", "type_idx": 15, "district_idx": 4, "status": "active", "priority": "high", "location_idx": 7},
        {"title": "Theft of copper cables", "desc": "Electrical cables stolen from construction site.", "type_idx": 0, "district_idx": 5, "status": "open", "priority": "medium", "location_idx": 0},
        {"title": "Arson at commercial building", "desc": "Fire set at shopping complex. Suspected insurance fraud.", "type_idx": 16, "district_idx": 0, "status": "active", "priority": "high", "location_idx": 2},
        {"title": "Kidnapping of minor in Kalaburagi", "desc": "School child kidnapped near bus stop. Ransom demanded.", "type_idx": 7, "district_idx": 5, "status": "active", "priority": "high", "location_idx": 0},
        {"title": "Extortion from hotel owners", "desc": "Threatening calls to hotel owners demanding protection money.", "type_idx": 13, "district_idx": 8, "status": "active", "priority": "high", "location_idx": 0},
    ]

    for i, row in enumerate(extra_crimes):
        existing = await get_one(db, Crime, title=row["title"])
        if existing:
            continue

        type_code = CRIME_TYPES[row["type_idx"]][1]
        district_code = DISTRICTS[row["district_idx"]][1]
        crime_type = await get_one(db, CrimeType, code=type_code)
        district = await get_one(db, District, code=district_code)

        day_offset = (i + len(CRIMES)) % 7
        hour = random.choice([1, 4, 7, 9, 12, 14, 17, 20, 23])
        occurred = base + timedelta(days=day_offset, hours=hour, minutes=random.randint(0, 59))

        db.add(Crime(
            title=row["title"],
            description=row["desc"],
            crime_type_id=crime_type.id if crime_type else None,
            district_id=district.id if district else None,
            location_id=None,
            status=row["status"],
            priority=row["priority"],
            occurred_at=occurred,
        ))
        n += 1

    await db.flush()
    return n
