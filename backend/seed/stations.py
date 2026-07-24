from seed.data import STATIONS
from seed.utils import ensure, get_one
from app.models.district import District
from app.models.state import State
from app.models.station import Station
from app.models.unit_type import UnitType


async def seed(db) -> int:
    ka = await get_one(db, State, code="KA")
    ps_type = await get_one(db, UnitType, code="PS")
    n = 0
    for name, code, district_code in STATIONS:
        district = await get_one(db, District, code=district_code)
        _, created = await ensure(
            db, Station,
            unique={"code": code},
            defaults={
                "name": name,
                "type": "police_station",
                "type_id": ps_type.id if ps_type else None,
                "state_id": ka.id if ka else None,
                "district_id": district.id if district else None,
                "address": f"{name}, Karnataka",
                "phone": "080-1000000",
                "active": True,
            },
        )
        n += int(created)
    return n
