from seed.data import CRIMES
from seed.utils import get_one
from app.models.case import Case
from app.models.complainant import Complainant
from app.models.gender import Gender
from app.models.occupation import Occupation
from app.models.religion import Religion


async def seed(db) -> int:
    male = await get_one(db, Gender, code="M")
    female = await get_one(db, Gender, code="F")
    occ = await get_one(db, Occupation, code="PVT")
    rel = await get_one(db, Religion, code="HIN")
    n = 0
    for i, _row in enumerate(CRIMES, start=1):
        case = await get_one(db, Case, case_number=f"CR/{i:04d}/2026")
        if not case:
            continue
        existing = await get_one(db, Complainant, case_id=case.id, name=f"Complainant {i}")
        if existing:
            continue
        gender = female if i % 2 == 0 else male
        db.add(Complainant(
            case_id=case.id,
            name=f"Complainant {i}",
            age_year=25 + (i % 40),
            occupation_id=occ.id if occ else None,
            religion_id=rel.id if rel else None,
            gender_id=gender.id if gender else None,
        ))
        n += 1
    await db.flush()
    return n
