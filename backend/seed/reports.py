from seed.utils import ensure, get_one
from app.models.report import Report
from app.models.user import User

ROWS = [
    ("Weekly Crime Summary — Bengaluru Urban", "summary", "draft"),
    ("Whitefield Murder — Investigation Report", "investigation", "draft"),
    ("Majestic Hotspot Analysis", "analytics", "completed"),
]


async def seed(db) -> int:
    user = await get_one(db, User, username="si.karthik")
    n = 0
    for title, rtype, status in ROWS:
        _, created = await ensure(
            db, Report,
            unique={"title": title},
            defaults={
                "type": rtype,
                "content": f"Seeded {rtype} report content for demo.",
                "format": "pdf",
                "generated_by": user.id if user else None,
                "status": status,
            },
        )
        n += int(created)
    return n
