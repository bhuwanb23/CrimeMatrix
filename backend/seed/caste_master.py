from seed.utils import ensure
from app.models.caste_master import CasteMaster

ROWS = [
    ("General", "GEN"),
    ("SC", "SC"),
    ("ST", "ST"),
    ("OBC", "OBC"),
    ("EWS", "EWS"),
    ("Other", "OTH"),
    ("Not Specified", "NS"),
]


async def seed(db) -> int:
    n = 0
    for name, code in ROWS:
        _, created = await ensure(db, CasteMaster, unique={"code": code}, defaults={"name": name})
        n += int(created)
    return n
