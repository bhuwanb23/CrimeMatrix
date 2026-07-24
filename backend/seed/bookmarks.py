from sqlalchemy import select

from seed.utils import get_one
from app.models.bookmark import Bookmark
from app.models.investigation import Investigation
from app.models.user import User


async def seed(db) -> int:
    user = await get_one(db, User, username="si.karthik")
    if not user:
        return 0
    investigations = (await db.execute(select(Investigation).limit(5))).scalars().all()
    n = 0
    for inv in investigations:
        existing = await get_one(db, Bookmark, user_id=user.id, investigation_id=inv.id)
        if existing:
            continue
        db.add(Bookmark(
            user_id=user.id,
            investigation_id=inv.id,
            entity_type="investigation",
            entity_id=inv.id,
            bookmark_note=f"Watchlist: {inv.title[:80]}",
        ))
        n += 1
    await db.flush()
    return n
