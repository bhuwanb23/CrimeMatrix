from seed.data import PERSONS
from seed.utils import ensure, get_one
from app.models.criminal import Criminal
from app.models.person import Person

CRIMINAL_ROWS = [
    (0, "Ravi", 78.5, "Chain snatching on motorcycle; targets crowded markets."),
    (1, "Ali", 65.0, "Vehicle theft; works with interstate fences."),
    (2, "Deepak", 82.0, "Organized robbery; silk and jewelry warehouses."),
    (4, "Suresh", 55.0, "NDPS manufacturing and distribution."),
    (6, "Imran", 70.0, "Port-linked narcotics logistics."),
]


async def seed(db) -> int:
    n = 0
    for person_idx, alias, risk, mo in CRIMINAL_ROWS:
        p = PERSONS[person_idx]
        person = await get_one(db, Person, first_name=p["first_name"], last_name=p["last_name"], phone=p["phone"])
        if not person:
            continue
        _, created = await ensure(
            db, Criminal,
            unique={"person_id": person.id},
            defaults={
                "alias": alias,
                "risk_score": risk,
                "status": "at_large",
                "mo_description": mo,
            },
        )
        n += int(created)
    return n
