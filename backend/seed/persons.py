from seed.data import PERSONS
from seed.utils import ensure
from app.models.person import Person


async def seed(db) -> int:
    n = 0
    for row in PERSONS:
        _, created = await ensure(
            db, Person,
            unique={"first_name": row["first_name"], "last_name": row["last_name"], "phone": row["phone"]},
            defaults={
                "gender": row["gender"],
                "district": row["district"],
            },
        )
        n += int(created)
    return n
