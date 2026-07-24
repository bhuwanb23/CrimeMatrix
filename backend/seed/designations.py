from seed.utils import ensure
from app.models.designation import Designation

ROWS = [
    ("Investigating Officer", "IO", 1),
    ("Station House Officer", "SHO", 2),
    ("Outgoing Officer", "OO", 3),
    ("Case Officer", "CO", 4),
    ("Supporting Officer", "SO", 5),
    ("Supervising Officer", "SUPO", 6),
]


async def seed(db) -> int:
    n = 0
    for name, code, sort_order in ROWS:
        _, created = await ensure(
            db, Designation,
            unique={"code": code},
            defaults={"name": name, "sort_order": sort_order, "active": True},
        )
        n += int(created)
    return n
