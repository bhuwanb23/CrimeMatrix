import asyncio
import sys
sys.path.insert(0, '.')

from sqlalchemy import select
from app.db.session import init_db, async_session
from app.models.crime import Crime
from app.models.person import Person
from app.models.criminal import Criminal
from app.models.district import District
from app.models.station import Station
from app.models.crimetype import CrimeType

DISTRICTS = [
    ("Bengaluru Urban", "BLR-U"), ("Bengaluru Rural", "BLR-R"),
    ("Mysuru", "MYS"), ("Mangaluru", "MNG"), ("Hubballi-Dharwad", "HUB"),
    ("Kalaburagi", "KLB"), ("Ballari", "BLY"), ("Vijayapura", "VJP"),
    ("Shivamogga", "SHV"), ("Davangere", "DVG"), ("Hassan", "HSM"),
    ("Mandya", "MDY"), ("Tumakuru", "TMK"), ("Kolar", "KLR"),
    ("Chikkaballapur", "CKB"), ("Ramanagara", "RMR"),
]

CRIME_TYPES = [
    ("Theft", "THR", 2), ("Robbery", "ROB", 3), ("Burglary", "BRG", 3),
    ("Murder", "MUR", 5), ("Assault", "ASL", 3), ("Fraud", "FRD", 2),
    ("Cybercrime", "CYB", 2), ("Kidnapping", "KID", 5), ("Drug Offense", "DRG", 3),
    ("Domestic Violence", "DV", 3), ("Hit and Run", "H&R", 3), ("Vehicle Theft", "VT", 2),
    ("Snatching", "SNCH", 3), ("Extortion", "EXT", 3), ("Forgery", "FRG", 2),
    ("Cheating", "CHT", 2), ("Arson", "ARS", 4), ("Rape", "RPE", 5),
]

STATIONS_PER_DISTRICT = {
    "Bengaluru Urban": ["Cubbon Park", "Shivajinagar", "Koramangala", "Indiranagar", "Whitefield"],
    "Mysuru": ["Nazarbad", "Vani Vilas Mohalla"],
    "Mangaluru": ["Mangalore South", "Mangalore North"],
    "Hubballi-Dharwad": ["Hubballi East", "Dharwad North"],
}

CRIMES = [
    {"title": "Armed robbery at jewelry store on MG Road", "desc": "Two suspects entered the store at 2:30 AM, threatened staff with knives, and stole gold jewelry worth Rs 15 lakhs. CCTV captured the incident.", "type_idx": 1, "district_idx": 0, "status": "open", "priority": "high"},
    {"title": "Chain snatching near Majestic Bus Stand", "desc": "Victim's gold chain snatched by two persons on a motorcycle. Incident occurred at 6:30 PM during rush hour.", "type_idx": 12, "district_idx": 0, "status": "open", "priority": "high"},
    {"title": "Mobile theft at Commercial Street", "desc": "iPhone 15 Pro stolen from victim's pocket while shopping. Suspect caught on nearby CCTV.", "type_idx": 0, "district_idx": 0, "status": "active", "priority": "medium"},
    {"title": "Burglary at Koramangala apartment", "desc": "House broken into through rear window. Laptop and gold chain stolen. No fingerprints found.", "type_idx": 2, "district_idx": 0, "status": "open", "priority": "medium"},
    {"title": "Murder case in Whitefield", "desc": "Body found in abandoned building. Victim identified as daily wage worker. Multiple stab wounds.", "type_idx": 3, "district_idx": 0, "status": "active", "priority": "high"},
    {"title": "Cyber fraud targeting senior citizens", "desc": "Multiple complaints of online banking fraud. Scammers posing as bank officials. Loss of Rs 8 lakhs.", "type_idx": 6, "district_idx": 0, "status": "active", "priority": "high"},
    {"title": "Drug seizure at bus stand", "desc": "1.5 kg of ganja seized from a passenger. Suspect arrested and remanded.", "type_idx": 8, "district_idx": 0, "status": "closed", "priority": "medium"},
    {"title": "Assault on traffic police", "desc": "Auto driver assaulted traffic constable during checking. Multiple witnesses.", "type_idx": 4, "district_idx": 0, "status": "closed", "priority": "medium"},
    {"title": "Vehicle theft from parking lot", "desc": "Honda City stolen from mall parking. GPS追踪 showed vehicle moved to Tamil Nadu border.", "type_idx": 11, "district_idx": 0, "status": "active", "priority": "high"},
    {"title": "Domestic violence complaint", "desc": "Wife filed complaint against husband for repeated assault. Medical report confirms injuries.", "type_idx": 9, "district_idx": 0, "status": "active", "priority": "medium"},
    {"title": "Hit and run near Hebbal flyover", "desc": "Pedestrian hit by speeding car. Driver fled. CCTV shows white sedan.", "type_idx": 10, "district_idx": 0, "status": "open", "priority": "high"},
    {"title": "Snatching at Forum Mall", "desc": "Woman's purse snatched by two persons on bike. Cash and cards stolen.", "type_idx": 12, "district_idx": 0, "status": "open", "priority": "medium"},
    {"title": "Extortion call to businessman", "desc": "Threatening call demanding Rs 10 lakhs. Caller claimed to be from organized crime group.", "type_idx": 13, "district_idx": 0, "status": "active", "priority": "high"},
    {"title": "Forgery of property documents", "desc": "Fake sale deed created for ancestral property. Multiple families affected.", "type_idx": 14, "district_idx": 0, "status": "open", "priority": "medium"},
    {"title": "Cheating in online job portal", "desc": "Multiple victims cheated of registration fees. Fake company operating from rented office.", "type_idx": 15, "district_idx": 0, "status": "active", "priority": "medium"},
    {"title": "Burglary at electronics shop", "desc": "Shop broken into at night. Laptops and phones worth Rs 5 lakhs stolen.", "type_idx": 2, "district_idx": 0, "status": "open", "priority": "medium"},
    {"title": "Robbery at ATM booth", "desc": "Armed robbery at ATM. Customer threatened and cash stolen.", "type_idx": 1, "district_idx": 0, "status": "open", "priority": "high"},
    {"title": "Vehicle theft from hospital", "desc": "Two-wheeler stolen from hospital parking. Lock broken.", "type_idx": 11, "district_idx": 0, "status": "open", "priority": "medium"},
    {"title": "Kidnapping attempt near school", "desc": "Attempt to kidnap school girl. locals intervened and suspect fled.", "type_idx": 7, "district_idx": 0, "status": "active", "priority": "high"},
    {"title": "Arson at warehouse", "desc": "Fire set at abandoned warehouse. Suspect known rival owner.", "type_idx": 16, "district_idx": 0, "status": "open", "priority": "high"},
    {"title": "Robbery at silk warehouse in Mysuru", "desc": "Cash and silk worth Rs 50 lakhs stolen. Inside job suspected.", "type_idx": 1, "district_idx": 2, "status": "active", "priority": "high"},
    {"title": "Theft at Mysuru Palace tourist area", "desc": "Tourist's bag snatched. CCTV shows two suspects on bike.", "type_idx": 0, "district_idx": 2, "status": "open", "priority": "medium"},
    {"title": "Cyber fraud via fake OLX listing", "desc": "Victim paid advance for fake OLX listing. Rs 2 lakhs lost.", "type_idx": 6, "district_idx": 2, "status": "active", "priority": "medium"},
    {"title": "Assault at Mysuru railway station", "desc": "Altercation between two groups. One person injured.", "type_idx": 4, "district_idx": 2, "status": "closed", "priority": "low"},
    {"title": "Drug peddling near Mangaluru port", "desc": "Contraband seized from shipping container. Two arrested.", "type_idx": 8, "district_idx": 3, "status": "closed", "priority": "high"},
    {"title": "Burglary at Mangaluru jewelry shop", "desc": "Shop broken into at night. Gold ornaments stolen.", "type_idx": 2, "district_idx": 3, "status": "open", "priority": "medium"},
    {"title": "Robbery at Hubballi bus depot", "desc": "Cash stolen from ticket counter. Employee involved.", "type_idx": 1, "district_idx": 4, "status": "active", "priority": "medium"},
    {"title": "Theft of cattle in Dharwad", "desc": "Three cattle stolen from farm. Suspects traced to neighboring district.", "type_idx": 0, "district_idx": 4, "status": "open", "priority": "medium"},
    {"title": "Fraud in cooperative bank", "desc": "Manager embezzled Rs 2 crores. Multiple accounts manipulated.", "type_idx": 5, "district_idx": 4, "status": "active", "priority": "high"},
    {"title": "Murder in Kalaburagi village", "desc": "Farmers' dispute turned violent. One dead, two injured.", "type_idx": 3, "district_idx": 5, "status": "active", "priority": "high"},
    {"title": "Vehicle theft ring busted", "desc": "Gang operating across Bellari and Ballari districts. 12 vehicles recovered.", "type_idx": 11, "district_idx": 6, "status": "closed", "priority": "high"},
    {"title": "Kidnapping for ransom in Vijayapura", "desc": "Businessman kidnapped. Rs 50 lakhs ransom demanded. Rescue operation launched.", "type_idx": 7, "district_idx": 7, "status": "active", "priority": "high"},
    {"title": "Arson at Shivamogga temple", "desc": "Temple set on fire. Sacred idols damaged. Community outrage.", "type_idx": 16, "district_idx": 8, "status": "active", "priority": "high"},
    {"title": "Cheating in real estate deal", "desc": "Multiple families cheated of advance payments. Fake property documents.", "type_idx": 15, "district_idx": 9, "status": "open", "priority": "medium"},
    {"title": "Domestic violence in Hassan", "desc": "Repeated assault reported by victim. Medical evidence collected.", "type_idx": 9, "district_idx": 10, "status": "active", "priority": "medium"},
    {"title": "Drug racket in Mandya", "desc": "Illegal drug manufacturing unit busted. Three arrested.", "type_idx": 8, "district_idx": 11, "status": "closed", "priority": "high"},
    {"title": "Theft of temple donations in Tumakuru", "desc": "Cash box stolen from temple. Temple priest suspected.", "type_idx": 0, "district_idx": 12, "status": "open", "priority": "medium"},
    {"title": "Hit and run in Kolar", "desc": "Two-wheeler rider hit by car. Driver fled scene.", "type_idx": 10, "district_idx": 13, "status": "open", "priority": "high"},
    {"title": "Forgery of educational certificates", "desc": "Fake SSLC certificates being sold. Multiple victims.", "type_idx": 14, "district_idx": 14, "status": "active", "priority": "medium"},
    {"title": "Extortion by fake police officer", "desc": "Person impersonating police demanding money from shopkeepers.", "type_idx": 13, "district_idx": 15, "status": "active", "priority": "high"},
]


async def seed():
    await init_db()
    async with async_session() as db:
        # Seed districts
        for name, code in DISTRICTS:
            existing = (await db.execute(
                select(District).where(District.name == name)
            )).scalar_one_or_none()
            if not existing:
                db.add(District(name=name, code=code))

        # Seed crime types
        for name, code, severity in CRIME_TYPES:
            existing = (await db.execute(
                select(CrimeType).where(CrimeType.code == code)
            )).scalar_one_or_none()
            if not existing:
                db.add(CrimeType(name=name, code=code, severity_level=severity))

        await db.commit()

        # Seed crimes
        count = 0
        for crime_data in CRIMES:
            district_result = await db.execute(select(District).offset(crime_data["district_idx"]).limit(1))
            district = district_result.scalar_one_or_none()
            ct_result = await db.execute(select(CrimeType).offset(crime_data["type_idx"]).limit(1))
            crime_type = ct_result.scalar_one_or_none()

            existing = (await db.execute(
                select(Crime).where(Crime.title == crime_data["title"])
            )).scalar_one_or_none()

            if not existing:
                db.add(Crime(
                    title=crime_data["title"],
                    description=crime_data["desc"],
                    crime_type_id=crime_type.id if crime_type else None,
                    district_id=district.id if district else None,
                    status=crime_data["status"],
                    priority=crime_data["priority"],
                ))
                count += 1

        await db.commit()
        print(f"Seeded {count} new crimes")

        # Verify
        result = await db.execute(select(Crime))
        total = len(result.scalars().all())
        print(f"Total crimes in database: {total}")


if __name__ == "__main__":
    asyncio.run(seed())
