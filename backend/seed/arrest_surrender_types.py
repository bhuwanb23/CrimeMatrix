from seed.utils import ensure
from app.models.arrest_surrender_type import ArrestSurrenderType

ROWS = [
    ("Arrest", "ARR", "Person arrested by police"),
    ("Voluntary Surrender", "SUR", "Voluntary surrender before police or court"),
    ("Surrender in Court", "SCT", "Surrender before court"),
]


async def seed(db) -> int:
    n = 0
    for name, code, desc in ROWS:
        _, created = await ensure(
            db, ArrestSurrenderType,
            unique={"code": code},
            defaults={"name": name, "description": desc},
        )
        n += int(created)
    return n
