from seed.utils import ensure
from app.models.act import Act

ROWS = [
    ("Indian Penal Code", "IPC", "IPC"),
    ("Bharatiya Nyaya Sanhita", "BNS", "BNS"),
    ("Code of Criminal Procedure", "CrPC", "CrPC"),
    ("Indian Evidence Act", "IEA", "IEA"),
    ("Narcotic Drugs and Psychotropic Substances Act", "NDPS", "NDPS"),
    ("Information Technology Act", "ITA", "ITA"),
    ("Arms Act", "ARM", "ARM"),
    ("Protection of Children from Sexual Offences Act", "POCSO", "POCSO"),
    ("Dowry Prohibition Act", "DPA", "DPA"),
    ("Motor Vehicles Act", "MVA", "MVA"),
    ("Excise Act", "EXC", "EXC"),
    ("Prevention of Corruption Act", "PCA", "PCA"),
]


async def seed(db) -> int:
    n = 0
    for name, code, act_code in ROWS:
        _, created = await ensure(
            db, Act,
            unique={"act_code": act_code},
            defaults={"name": name, "code": code, "short_name": code, "active": True},
        )
        n += int(created)
    return n
