from seed.utils import get_one
from app.models.act import Act
from app.models.section import Section

ROWS = [
    ("Murder", "302", "IPC"),
    ("Attempt to Murder", "307", "IPC"),
    ("Culpable Homicide", "304", "IPC"),
    ("Robbery", "392", "IPC"),
    ("Dacoity", "395", "IPC"),
    ("Theft", "379", "IPC"),
    ("Burglary", "454", "IPC"),
    ("Cheating", "420", "IPC"),
    ("Criminal Intimidation", "506", "IPC"),
    ("Assault", "323", "IPC"),
    ("Kidnapping", "363", "IPC"),
    ("Rape", "376", "IPC"),
    ("Dowry Death", "304B", "IPC"),
    ("Cruelty by Husband", "498A", "IPC"),
    ("Arson", "435", "IPC"),
    ("Criminal Breach of Trust", "406", "IPC"),
    ("Forging Documents", "465", "IPC"),
    ("Hacking", "66", "ITA"),
    ("Drug Trafficking", "20", "NDPS"),
    ("Drug Possession", "8", "NDPS"),
    ("Arms Possession", "25", "ARM"),
    ("POCSO Offence", "4", "POCSO"),
    ("Stalking", "354D", "IPC"),
    ("Outraging Modesty", "354", "IPC"),
]


async def seed(db) -> int:
    n = 0
    for name, section_code, act_code in ROWS:
        act = await get_one(db, Act, act_code=act_code)
        act_id = act.id if act else None
        if act_id and await get_one(db, Section, section_code=section_code, act_id=act_id):
            continue
        if not act_id and await get_one(db, Section, section_code=section_code):
            continue
        db.add(Section(
            name=name,
            code=section_code,
            section_code=section_code,
            act_id=act_id,
            description=f"Section {section_code}",
            active=True,
        ))
        n += 1
    await db.flush()
    return n
