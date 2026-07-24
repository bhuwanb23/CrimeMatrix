from seed.utils import ensure
from app.models.gender import Gender

ROWS = [
    ("Male", "M"),
    ("Female", "F"),
    ("Transgender", "T"),
    ("Other", "O"),
    ("Not Specified", "NS"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, Gender, unique={"code": code}, defaults={"name": name})
        n += int(created)
    return n
