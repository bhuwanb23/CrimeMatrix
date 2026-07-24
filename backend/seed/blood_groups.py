from seed.utils import ensure
from app.models.blood_group import BloodGroup

ROWS = [("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"), ("AB+", "AB+"), ("AB-", "AB-"), ("O+", "O+"), ("O-", "O-")]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, BloodGroup, unique={"code": code}, defaults={"name": name})
        n += int(created)
    return n
