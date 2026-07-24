from seed.utils import ensure, get_one
from app.models.crime_head import CrimeHead
from app.models.crime_sub_head import CrimeSubHead

ROWS = [
    ("Murder", "MUR", "OAB"),
    ("Attempt to Murder", "ATM", "OAB"),
    ("Culpable Homicide", "CHM", "OAB"),
    ("Assault", "AST", "OAB"),
    ("Kidnapping", "KID", "OAB"),
    ("Robbery", "ROB", "OAP"),
    ("Burglary", "BRG", "OAP"),
    ("Theft", "THF", "OAP"),
    ("Criminal Breach of Trust", "CBT", "OAP"),
    ("Rape", "RAP", "OAW"),
    ("Dowry Death", "DWD", "OAW"),
    ("Acid Attack", "ACD", "OAW"),
    ("Child Labour", "CHL", "OAC"),
    ("POCSO", "PCS", "OAC"),
    ("Cheating", "CHT", "ECO"),
    ("Forgery", "FRG", "ECO"),
    ("Money Laundering", "MLN", "ECO"),
    ("Hacking", "HCK", "CYO"),
    ("Identity Theft", "IDT", "CYO"),
    ("Drug Trafficking", "DTF", "NDP"),
    ("Drug Possession", "DPS", "NDP"),
    ("Arms Possession", "ARMP", "ARM"),
    ("Unlawful Assembly", "ULA", "ARM"),
    ("Other", "OTH", "OTH"),
]


async def seed(db) -> int:
    n = 0
    for name, code, head_code in ROWS:
        head = await get_one(db, CrimeHead, code=head_code)
        _, created = await ensure(
            db, CrimeSubHead,
            unique={"code": code},
            defaults={"name": name, "crime_head_id": head.id if head else None},
        )
        n += int(created)
    return n
