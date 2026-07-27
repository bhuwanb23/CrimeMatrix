from seed.utils import ensure
from app.models.alert import Alert

ROWS = [
    ("whisper", "FIR match across districts", "Similar MO detected between Bengaluru and Mysuru robbery cases.", "high", "new", "Bengaluru Urban"),
    ("cross-district", "Vehicle tracking alert", "Suspect vehicle KA-01-AB-1234 spotted near Hubballi.", "high", "new", "Hubballi-Dharwad"),
    ("evidence", "CCTV linked to Whitefield murder", "New footage from ITPL parking matches timeline.", "medium", "pending", "Bengaluru Urban"),
    ("ai", "Hotspot escalation — Majestic", "Predictive spike in snatching incidents next 48h.", "high", "new", "Bengaluru Urban"),
    ("fir-match", "Suspect vehicle match", "KA-05 plate linked to open vehicle theft cases.", "medium", "pending", "Mysuru"),
    ("ai", "Burglary spike — Koramangala", "Weekend burglary rate exceeding 30-day baseline.", "high", "new", "Bengaluru Urban"),
    ("cross-district", "Suspect movement — Mangaluru to Mysuru", "Known NDPS suspect spotted on coastal highway cameras.", "high", "new", "Mangaluru"),
    ("evidence", "Fingerprint match — ATM robbery", "Latent print matches open ATM robbery file.", "high", "pending", "Bengaluru Urban"),
    ("whisper", "MO match — silk warehouse cases", "Similar entry method across Mysuru property crimes.", "medium", "new", "Mysuru"),
    ("ai", "Festival crowd risk — Commercial Street", "Predicted theft/snatching surge during weekend footfall.", "high", "new", "Bengaluru Urban"),
    ("fir-match", "Phone IMEI hit", "Stolen phone IMEI resurfaced near Hubballi tower.", "medium", "pending", "Hubballi-Dharwad"),
    ("evidence", "DNA pending — Whitefield murder", "Lab queue delay flagged for high-priority case.", "medium", "pending", "Bengaluru Urban"),
    ("cross-district", "Cattle theft trail", "Suspect vehicle tracked toward neighboring district.", "medium", "new", "Hubballi-Dharwad"),
    ("ai", "Cyber fraud campaign", "Cluster of senior-citizen banking fraud complaints.", "high", "new", "Bengaluru Urban"),
    ("whisper", "Extortion network signal", "Shared caller ID across shopkeeper complaints.", "high", "new", "Ramanagara"),
    ("fir-match", "Fake certificate batch", "Same printer watermark across forgery complaints.", "medium", "pending", "Kolar"),
    ("ai", "Hit-and-run pattern — Kolar road", "Night-time hit-and-run frequency rising.", "high", "new", "Kolar"),
    ("evidence", "Warehouse CCTV recovered", "New angle of arson suspect near Whitefield warehouse.", "medium", "new", "Bengaluru Urban"),
    ("cross-district", "Kidnap ransom SIM", "Ransom SIM used earlier in Vijayapura case.", "critical", "new", "Vijayapura"),
    ("ai", "Drug seizure forecast — Port", "Elevated risk window for port-linked NDPS activity.", "high", "pending", "Mangaluru"),
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
