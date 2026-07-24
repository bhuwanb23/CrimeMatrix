from seed.utils import ensure
from app.models.state import State

ROWS = [
    ("Karnataka", "KA"),
    ("Maharashtra", "MH"),
    ("Tamil Nadu", "TN"),
    ("Kerala", "KL"),
    ("Andhra Pradesh", "AP"),
    ("Telangana", "TS"),
    ("Goa", "GA"),
    ("Puducherry", "PY"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, State, unique={"code": code}, defaults={"name": name, "active": True})
        n += int(created)
    return n
