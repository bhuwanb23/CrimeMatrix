from seed.utils import ensure
from app.models.report import ReportTemplate

ROWS = [
    ("Case Summary", "Executive summary of investigation findings", "# Case Summary\n\n{{title}}\n\n{{facts}}"),
    ("Timeline Report", "Chronological event timeline", "# Timeline\n\n{{events}}"),
    ("Evidence Inventory", "List of collected evidence", "# Evidence\n\n{{evidence}}"),
    ("Investigation Brief", "Officer briefing pack", "# Brief\n\n{{brief}}"),
]


async def seed(db) -> int:
    n = 0
    for name, desc, content in ROWS:
        _, created = await ensure(
            db, ReportTemplate,
            unique={"name": name},
            defaults={"description": desc, "template_content": content, "is_active": True},
        )
        n += int(created)
    return n
