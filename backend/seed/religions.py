from seed.utils import ensure
from app.models.religion import Religion

ROWS = [
    ("Hindu", "HIN"),
    ("Muslim", "MUS"),
    ("Christian", "CHR"),
    ("Sikh", "SIK"),
    ("Buddhist", "BUD"),
    ("Jain", "JAI"),
    ("Other", "OTH"),
    ("Not Specified", "NS"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, Religion, unique={"code": code}, defaults={"name": name})
        n += int(created)
    return n
