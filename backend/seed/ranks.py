from seed.utils import ensure
from app.models.rank import Rank

ROWS = [
    ("Constable", "CON", 10),
    ("Head Constable", "HC", 9),
    ("Assistant Sub-Inspector", "ASI", 8),
    ("Sub-Inspector", "SI", 7),
    ("Inspector", "INS", 6),
    ("Deputy Superintendent of Police", "DSP", 5),
    ("Superintendent of Police", "SP", 4),
    ("Deputy Inspector General", "DIG", 3),
    ("Inspector General", "IG", 2),
    ("Director General of Police", "DGP", 1),
]


async def seed(db) -> int:
    n = 0
    for name, code, hierarchy in ROWS:
        _, created = await ensure(
            db, Rank,
            unique={"code": code},
            defaults={"name": name, "hierarchy": hierarchy, "active": True},
        )
        n += int(created)
    return n
