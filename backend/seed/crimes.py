from datetime import datetime, timedelta, timezone

from seed.data import CRIMES, CRIME_TYPES, DISTRICTS, LOCATIONS
from seed.utils import get_one
from app.models.crime import Crime
from app.models.crimetype import CrimeType
from app.models.district import District
from app.models.location import Location


async def seed(db) -> int:
    n = 0
    base = datetime.now(timezone.utc) - timedelta(days=60)
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

        db.add(Crime(
            title=row["title"],
            description=row["desc"],
            crime_type_id=crime_type.id if crime_type else None,
            district_id=district.id if district else None,
            location_id=location_id,
            status=row["status"],
            priority=row["priority"],
            occurred_at=base + timedelta(days=i, hours=i % 12),
        ))
        n += 1

    await db.flush()
    return n
