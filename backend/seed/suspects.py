from seed.data import SUSPECTS
from seed.utils import ensure
from app.models.suspect import Suspect


async def seed(db) -> int:
    n = 0
    for row in SUSPECTS:
        _, created = await ensure(
            db, Suspect,
            unique={"name": row["name"]},
            defaults={
                "age": row["age"],
                "gender": row["gender"],
                "district": row["district"],
                "status": row["status"],
                "risk_score": row["risk_score"],
                "description": row["description"],
                "aliases": row["aliases"],
            },
        )
        n += int(created)
    return n
