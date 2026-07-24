from seed.utils import ensure
from app.models.alert import Alert

ROWS = [
    ("whisper", "FIR match across districts", "Similar MO detected between Bengaluru and Mysuru robbery cases.", "high", "new", "Bengaluru Urban"),
    ("cross-district", "Vehicle tracking alert", "Suspect vehicle KA-01-AB-1234 spotted near Hubballi.", "high", "new", "Hubballi-Dharwad"),
    ("evidence", "CCTV linked to Whitefield murder", "New footage from ITPL parking matches timeline.", "medium", "pending", "Bengaluru Urban"),
    ("ai", "Hotspot escalation — Majestic", "Predictive spike in snatching incidents next 48h.", "high", "new", "Bengaluru Urban"),
    ("fir-match", "Suspect vehicle match", "KA-05 plate linked to open vehicle theft cases.", "medium", "pending", "Mysuru"),
]


async def seed(db) -> int:
    n = 0
    for alert_type, title, desc, priority, status, district in ROWS:
        _, created = await ensure(
            db, Alert,
            unique={"title": title},
            defaults={
                "alert_type": alert_type,
                "description": desc,
                "priority": priority,
                "status": status,
                "district": district,
                "is_read": False,
            },
        )
        n += int(created)
    return n
