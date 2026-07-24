from seed.data import OFFICERS
from seed.utils import ensure, get_one
from app.models.designation import Designation
from app.models.district import District
from app.models.gender import Gender
from app.models.officer import Officer
from app.models.rank import Rank
from app.models.station import Station


async def seed(db) -> int:
    io = await get_one(db, Designation, code="IO")
    male = await get_one(db, Gender, code="M")
    female = await get_one(db, Gender, code="F")
    n = 0
    for row in OFFICERS:
        rank = await get_one(db, Rank, code=row["rank_code"])
        station = await get_one(db, Station, code=row["station_code"])
        district = await get_one(db, District, code=row["district_code"])
        gender = female if row["first_name"] in ("Meena", "Fatima") else male
        _, created = await ensure(
            db, Officer,
            unique={"badge_number": row["badge_number"]},
            defaults={
                "kgid": row["kgid"],
                "first_name": row["first_name"],
                "rank": rank.name if rank else row["rank_code"],
                "rank_id": rank.id if rank else None,
                "unit_id": station.id if station else None,
                "station_id": station.id if station else None,
                "designation_id": io.id if io else None,
                "district_id": district.id if district else None,
                "gender_id": gender.id if gender else None,
                "phone": row["phone"],
                "status": "active",
            },
        )
        n += int(created)
    return n
