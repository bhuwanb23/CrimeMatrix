from seed.utils import ensure
from app.models.case_status_master import CaseStatusMaster

ROWS = [
    ("Registered", "REG"),
    ("Under Investigation", "INV"),
    ("Charge Sheet Filed", "CHS"),
    ("Convicted", "CONV"),
    ("Acquitted", "ACQ"),
    ("Closed", "CLS"),
    ("Transferred", "XFR"),
    ("Abated", "ABT"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, CaseStatusMaster, unique={"code": code}, defaults={"name": name})
        n += int(created)
    return n
