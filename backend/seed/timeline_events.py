from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from seed.utils import get_one
from app.models.investigation import Investigation
from app.models.timeline_event import TimelineEvent

EVENT_TEMPLATES = [
    ("FIR Registered", "fir_filed"),
    ("Scene Inspection", "inspection"),
    ("Witness Statement", "statement"),
    ("Evidence Collected", "evidence"),
    ("Suspect Identified", "suspect"),
]


async def seed(db) -> int:
    investigations = (await db.execute(select(Investigation))).scalars().all()
    n = 0
    base = datetime.now(timezone.utc) - timedelta(days=30)
    for inv in investigations:
        for j, (title, etype) in enumerate(EVENT_TEMPLATES):
            full_title = f"{title} — INV-{inv.id}"
            if await get_one(db, TimelineEvent, investigation_id=inv.id, title=full_title):
                continue
            db.add(TimelineEvent(
                investigation_id=inv.id,
                title=full_title,
                description=f"{title} recorded for {inv.title}",
                event_type=etype,
                event_date=base + timedelta(days=j * 2, hours=inv.id),
            ))
            n += 1
    await db.flush()
    return n
