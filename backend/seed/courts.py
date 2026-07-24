from seed.utils import ensure
from app.models.court import Court

ROWS = [
    ("Sessions Court Bengaluru", "SCBNG", "Bengaluru Urban", "Sessions"),
    ("Sessions Court Mysuru", "SCMYS", "Mysuru", "Sessions"),
    ("Sessions Court Mangaluru", "SCMNG", "Mangaluru", "Sessions"),
    ("JMFC Court Bengaluru", "JMBNG", "Bengaluru Urban", "JMFC"),
    ("JMFC Court Mysuru", "JMMYS", "Mysuru", "JMFC"),
    ("Special Court (NDPS) Bengaluru", "SCNDPS", "Bengaluru Urban", "Special"),
    ("Fast Track Court Bengaluru", "FTCBNG", "Bengaluru Urban", "Fast Track"),
    ("Family Court Bengaluru", "FCBNG", "Bengaluru Urban", "Family"),
]


async def seed(db) -> int:
    n = 0
    for name, code, district, ctype in ROWS:
        _, created = await ensure(
            db, Court,
            unique={"code": code},
            defaults={"name": name, "district": district, "court_type": ctype, "active": True},
        )
        n += int(created)
    return n
