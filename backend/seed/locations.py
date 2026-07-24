from seed.data import LOCATIONS
from seed.utils import ensure, get_one
from app.models.district import District
from app.models.location import Location


async def seed(db) -> int:
    n = 0
    for name, address, lat, lng, district_code, loc_type in LOCATIONS:
        district = await get_one(db, District, code=district_code)
        _, created = await ensure(
            db, Location,
            unique={"name": name},
            defaults={
                "address": address,
                "latitude": lat,
                "longitude": lng,
                "district_id": district.id if district else None,
                "type": loc_type,
            },
        )
        n += int(created)
    return n
