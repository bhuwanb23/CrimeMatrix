from seed.utils import ensure
from app.models.gravity_offence import GravityOffence

ROWS = [
    ("Murder", "MUR", 10),
    ("Rape", "RAP", 9),
    ("Robbery", "ROB", 7),
    ("Dacoity", "DAC", 8),
    ("Kidnapping", "KID", 7),
    ("Arson", "ARS", 6),
    ("Assault", "ASS", 5),
    ("Theft", "THF", 4),
    ("Fraud", "FRD", 4),
    ("Cybercrime", "CYB", 5),
    ("Drug Offence", "DRG", 6),
    ("General", "GEN", 1),
]


async def seed(db) -> int:
    n = 0
    for name, code, sev in ROWS:
        _, created = await ensure(
            db, GravityOffence,
            unique={"code": code},
            defaults={"name": name, "severity_level": sev, "active": True},
        )
        n += int(created)
    return n
