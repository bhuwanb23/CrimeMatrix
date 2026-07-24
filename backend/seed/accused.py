from seed.data import CRIMES, SUSPECTS
from seed.utils import get_one
from app.models.accused import Accused
from app.models.case import Case
from app.models.gender import Gender


async def seed(db) -> int:
    male = await get_one(db, Gender, code="M")
    female = await get_one(db, Gender, code="F")
    n = 0
    # Attach a rotating suspect name as accused on each case
    for i, _row in enumerate(CRIMES, start=1):
        case = await get_one(db, Case, case_number=f"CR/{i:04d}/2026")
        if not case:
            continue
        suspect = SUSPECTS[(i - 1) % len(SUSPECTS)]
        name = suspect["name"]
        existing = await get_one(db, Accused, case_id=case.id, name=name)
        if existing:
            continue
        gender = female if suspect["gender"] == "Female" else male
        db.add(Accused(
            case_id=case.id,
            name=name,
            age_year=suspect["age"],
            gender_id=gender.id if gender else None,
        ))
        n += 1
    await db.flush()
    return n
