from seed.utils import ensure
from app.models.occupation import Occupation

ROWS = [
    ("Government Employee", "GOV"),
    ("Private Employee", "PVT"),
    ("Business", "BIZ"),
    ("Student", "STD"),
    ("Farmer", "FAR"),
    ("Daily Wage Worker", "DWG"),
    ("Professional", "PRF"),
    ("Retired", "RET"),
    ("Unemployed", "UNEMP"),
    ("Homemaker", "HOME"),
    ("Driver", "DRV"),
    ("Housewife", "HSW"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, Occupation, unique={"code": code}, defaults={"name": name})
        n += int(created)
    return n
