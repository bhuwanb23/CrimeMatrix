from seed.data import CRIMES
from seed.utils import get_one
from app.models.case import Case
from app.models.gender import Gender
from app.models.victim import Victim


async def seed(db) -> int:
    male = await get_one(db, Gender, code="M")
    female = await get_one(db, Gender, code="F")
    n = 0
    for i, _row in enumerate(CRIMES, start=1):
        case = await get_one(db, Case, case_number=f"CR/{i:04d}/2026")
        if not case:
            continue
        name = f"Victim {i}"
        existing = await get_one(db, Victim, case_id=case.id, name=name)
        if existing:
            continue
        gender = female if i % 3 == 0 else male
        db.add(Victim(
            case_id=case.id,
            name=name,
            age_year=20 + (i % 50),
            gender_id=gender.id if gender else None,
            is_police=(i % 17 == 0),
        ))
        n += 1
    await db.flush()
    return n
