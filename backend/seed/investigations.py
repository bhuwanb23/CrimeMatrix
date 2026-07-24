from datetime import datetime, timezone

from seed.data import CRIMES
from seed.utils import get_one
from app.models.case import Case
from app.models.investigation import Investigation
from app.models.user import User

# Seed investigations for the first N cases
INVESTIGATION_COUNT = 15


async def seed(db) -> int:
    user = await get_one(db, User, username="si.karthik")
    n = 0
    for i, row in enumerate(CRIMES[:INVESTIGATION_COUNT], start=1):
        case = await get_one(db, Case, case_number=f"CR/{i:04d}/2026")
        if not case:
            continue
        title = f"Investigation — {row['title'][:80]}"
        existing = await get_one(db, Investigation, title=title)
        if existing:
            continue
        db.add(Investigation(
            case_id=case.id,
            title=title,
            description=row["desc"],
            status="active" if row["status"] != "closed" else "saved",
            priority=row["priority"] if row["priority"] != "low" else "medium",
            officer_id=user.id if user else None,
            progress=min(90, 10 + i * 5),
            district=case.district,
            last_accessed=datetime.now(timezone.utc),
        ))
        n += 1
    await db.flush()
    return n
