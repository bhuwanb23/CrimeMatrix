from seed.utils import ensure
from app.models.crime_head import CrimeHead

ROWS = [
    ("Offences Against Body", "OAB"),
    ("Offences Against Property", "OAP"),
    ("Offences Against Women", "OAW"),
    ("Offences Against Children", "OAC"),
    ("Economic Offences", "ECO"),
    ("Cyber Offences", "CYO"),
    ("NDPS Offences", "NDP"),
    ("Arms Act Offences", "ARM"),
    ("Excise Offences", "EXC"),
    ("Other Offences", "OTH"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(
            db, CrimeHead,
            unique={"code": code},
            defaults={"name": name, "active": True},
        )
        n += int(created)
    return n
