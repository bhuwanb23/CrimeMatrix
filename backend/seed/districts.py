from seed.data import DISTRICTS
from seed.utils import ensure, get_one
from app.models.district import District
from app.models.state import State


async def seed(db) -> int:
    ka = await get_one(db, State, code="KA")
    n = 0
    for name, code in DISTRICTS:
        _, created = await ensure(
            db, District,
            unique={"code": code},
            defaults={
                "name": name,
                "state": "Karnataka",
                "state_id": ka.id if ka else None,
                "active": True,
            },
        )
        n += int(created)
    return n
