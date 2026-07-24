from seed.utils import ensure
from app.models.case_category import CaseCategory

ROWS = [
    ("FIR", "FIR", "First Information Report"),
    ("Zero FIR", "ZFIR", "Zero FIR — filed at any station"),
    ("UDR", "UDR", "Untraced Daily Report"),
    ("PAR", "PAR", "Prosecution Against Register"),
    ("NCR", "NCR", "Non-Cognizable Report"),
]


async def seed(db) -> int:
    n = 0
    for name, code, desc in ROWS:
        _, created = await ensure(
            db, CaseCategory,
            unique={"code": code},
            defaults={"name": name, "description": desc, "active": True},
        )
        n += int(created)
    return n
