from seed.utils import get_one
from app.models.crimetype import CrimeType
from app.models.district import District
from app.models.early_warning_alert import EarlyWarningAlert

ROWS = [
    ("spike", "Theft spike in Bengaluru Urban", "Theft complaints up 40% vs 30-day baseline.", "high", "BLR-U", "THR", 42, 25, 82),
    ("hotspot", "Snatching hotspot near Majestic", "Cluster of snatching events within 1km radius.", "critical", "BLR-U", "SNCH", 18, 8, 90),
    ("serial", "Serial burglary pattern — Koramangala", "MO fingerprint matches 4 open burglaries.", "high", "BLR-U", "BRG", 4, 3, 75),
    ("escalation", "Drug trafficking escalation — Mangaluru", "Port-linked seizures rising for 3 weeks.", "medium", "MNG", "DRG", 6, 3, 68),
    ("spike", "Robbery uptick — Mysuru", "Weekend robberies exceeding threshold.", "high", "MYS", "ROB", 9, 5, 71),
    ("spike", "Vehicle theft spike — Whitefield", "IT campus parking thefts up vs baseline.", "high", "BLR-U", "VT", 14, 7, 77),
    ("hotspot", "Cyber fraud cluster — MG Road", "Senior-targeted banking fraud density rising.", "critical", "BLR-U", "CYB", 11, 4, 88),
    ("serial", "ATM robbery series", "Shared MO across three ATM robberies.", "high", "BLR-U", "ROB", 3, 2, 80),
    ("escalation", "Extortion calls — Ramanagara", "Shopkeeper complaints with shared caller pattern.", "high", "RMR", "EXT", 8, 3, 74),
    ("spike", "Assault complaints — Hubballi", "Night assault reports above threshold.", "medium", "HUB", "ASL", 10, 6, 65),
    ("hotspot", "Tourist theft — Mysuru Palace", "Tourist-targeted theft density elevated.", "medium", "MYS", "THR", 7, 3, 70),
    ("serial", "Forgery certificate batch", "Same watermark across SSLC forgery reports.", "medium", "CKB", "FRG", 5, 2, 72),
    ("escalation", "NDPS Mandya corridor", "Manufacturing/distribution signals rising.", "high", "MDY", "DRG", 6, 2, 79),
    ("spike", "Hit-and-run — Kolar highway", "Night hit-and-run frequency above baseline.", "high", "KLR", "H&R", 5, 2, 76),
    ("hotspot", "Cattle theft belt — Dharwad", "Farm cattle theft cluster expanding.", "medium", "HUB", "THR", 6, 3, 67),
]


async def seed(db) -> int:
    n = 0
    for alert_type, title, desc, severity, dcode, tcode, detected, threshold, confidence in ROWS:
        if await get_one(db, EarlyWarningAlert, title=title):
            continue
        district = await get_one(db, District, code=dcode)
        crime_type = await get_one(db, CrimeType, code=tcode)
        db.add(EarlyWarningAlert(
            alert_type=alert_type,
            title=title,
            description=desc,
            severity=severity,
            district_id=district.id if district else None,
            crime_type_id=crime_type.id if crime_type else None,
            detected_value=float(detected),
            threshold=float(threshold),
            confidence=float(confidence),
            status="active",
        ))
        n += 1
    await db.flush()
    return n
