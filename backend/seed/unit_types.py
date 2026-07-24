from seed.utils import ensure
from app.models.unit_type import UnitType

ROWS = [
    ("Police Station", "PS", "City", 4, "Local police station"),
    ("Circle Office", "CO", "District", 3, "Circle-level police office"),
    ("Sub-Division", "SD", "District", 2, "Sub-divisional police office"),
    ("District Police", "DP", "District", 1, "District police headquarters"),
    ("Commissionerate", "CMP", "City", 1, "City police commissionerate"),
    ("State Headquarters", "SHQ", "State", 0, "State police headquarters"),
]


async def seed(db) -> int:
    n = 0
    for name, code, cds, hierarchy, desc in ROWS:
        _, created = await ensure(
            db, UnitType,
            unique={"code": code},
            defaults={"name": name, "city_dist_state": cds, "hierarchy": hierarchy, "description": desc, "active": True},
        )
        n += int(created)
    return n
