from sqlalchemy import select

from seed.utils import get_one
from app.models.investigation import Investigation
from app.models.note import Note
from app.models.user import User


async def seed(db) -> int:
    user = await get_one(db, User, username="si.karthik")
    investigations = (await db.execute(select(Investigation))).scalars().all()
    n = 0
    for inv in investigations:
        content = f"Initial case note for {inv.title}: scene visited, witnesses listed, evidence logged."
        existing = await get_one(db, Note, investigation_id=inv.id, content=content)
        if existing:
            continue
        db.add(Note(
            investigation_id=inv.id,
            content=content,
            author_id=user.id if user else None,
        ))
        n += 1
        follow = f"Follow-up: awaiting forensic report for investigation #{inv.id}."
        if not await get_one(db, Note, investigation_id=inv.id, content=follow):
            db.add(Note(
                investigation_id=inv.id,
                content=follow,
                author_id=user.id if user else None,
            ))
            n += 1
    await db.flush()
    return n
