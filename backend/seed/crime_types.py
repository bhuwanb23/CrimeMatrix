from seed.data import CRIME_TYPES
from seed.utils import ensure
from app.models.crimetype import CrimeType


async def seed(db) -> int:
    n = 0
    for name, code, severity in CRIME_TYPES:
        _, created = await ensure(
            db, CrimeType,
            unique={"code": code},
            defaults={"name": name, "severity_level": severity, "is_active": 1},
        )
        n += int(created)
    return n
