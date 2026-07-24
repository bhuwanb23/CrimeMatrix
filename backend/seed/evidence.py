from seed.data import CRIMES
from seed.utils import get_one
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.user import User

EVIDENCE_TYPES = ["cctv", "weapon", "document", "fingerprint", "phone_record", "forensic"]


async def seed(db) -> int:
    user = await get_one(db, User, username="si.karthik")
    n = 0
    for i, _row in enumerate(CRIMES, start=1):
        case = await get_one(db, Case, case_number=f"CR/{i:04d}/2026")
        if not case:
            continue
        etype = EVIDENCE_TYPES[i % len(EVIDENCE_TYPES)]
        desc = f"{etype.replace('_', ' ').title()} evidence for case {case.case_number}"
        existing = await get_one(db, Evidence, case_id=case.id, description=desc)
        if existing:
            continue
        db.add(Evidence(
            case_id=case.id,
            evidence_type=etype,
            description=desc,
            status="collected" if i % 3 else "pending",
            recorded_by=user.id if user else None,
        ))
        n += 1
    await db.flush()
    return n
