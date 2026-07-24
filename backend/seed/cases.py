"""Seed cases with explicit ids matching crimes so CaseMaster panels work from Search."""

from datetime import datetime, timedelta, timezone

from seed.data import CRIMES, CRIME_TYPES, DISTRICTS, STATIONS
from seed.utils import get_one
from app.models.case import Case
from app.models.case_category import CaseCategory
from app.models.case_status_master import CaseStatusMaster
from app.models.court import Court
from app.models.crime_head import CrimeHead
from app.models.crime_sub_head import CrimeSubHead
from app.models.fir import FIR
from app.models.gravity_offence import GravityOffence
from app.models.officer import Officer
from app.models.station import Station
from app.models.user import User

# Map crime type name → gravity / head / sub-head codes (best-effort)
TYPE_MAP = {
    "Theft": ("THF", "OAP", "THF"),
    "Robbery": ("ROB", "OAP", "ROB"),
    "Burglary": ("ROB", "OAP", "BRG"),
    "Murder": ("MUR", "OAB", "MUR"),
    "Assault": ("ASS", "OAB", "AST"),
    "Fraud": ("FRD", "ECO", "CHT"),
    "Cybercrime": ("CYB", "CYO", "HCK"),
    "Kidnapping": ("KID", "OAB", "KID"),
    "Drug Offense": ("DRG", "NDP", "DPS"),
    "Domestic Violence": ("ASS", "OAW", "AST"),
    "Hit and Run": ("GEN", "OTH", "OTH"),
    "Vehicle Theft": ("THF", "OAP", "THF"),
    "Snatching": ("THF", "OAP", "THF"),
    "Extortion": ("FRD", "ECO", "CHT"),
    "Forgery": ("FRD", "ECO", "FRG"),
    "Cheating": ("FRD", "ECO", "CHT"),
    "Arson": ("ARS", "OAP", "OTH"),
    "Rape": ("RAP", "OAW", "RAP"),
}


def _station_code(district_idx: int) -> str | None:
    dcode = DISTRICTS[district_idx][1]
    for _name, code, district_code in STATIONS:
        if district_code == dcode:
            return code
    return None


async def seed(db) -> int:
    user = await get_one(db, User, username="si.karthik")
    category = await get_one(db, CaseCategory, code="FIR")
    status_inv = await get_one(db, CaseStatusMaster, code="INV")
    status_cls = await get_one(db, CaseStatusMaster, code="CLS")
    court = await get_one(db, Court, code="SCBNG")
    officer = await get_one(db, Officer, badge_number="KSP-1001")

    n = 0
    base = datetime.now(timezone.utc) - timedelta(days=60)
    for i, row in enumerate(CRIMES, start=1):
        case_number = f"CR/{i:04d}/2026"
        existing = await get_one(db, Case, case_number=case_number)
        if existing:
            continue

        crime_type_name = CRIME_TYPES[row["type_idx"]][0]
        district_name = DISTRICTS[row["district_idx"]][0]
        g_code, h_code, s_code = TYPE_MAP.get(crime_type_name, ("GEN", "OTH", "OTH"))
        gravity = await get_one(db, GravityOffence, code=g_code)
        head = await get_one(db, CrimeHead, code=h_code)
        sub = await get_one(db, CrimeSubHead, code=s_code)
        fir = await get_one(db, FIR, fir_number=f"FIR/{i:04d}/2026")
        station_code = _station_code(row["district_idx"])
        station = await get_one(db, Station, code=station_code) if station_code else None
        case_status = status_cls if row["status"] == "closed" else status_inv

        db.add(Case(
            id=i,  # match crime.id for CaseDetail CaseMaster fetches
            case_number=case_number,
            crime_no=f"CN/{i:04d}/2026",
            title=row["title"],
            description=row["desc"],
            brief_facts=row["desc"],
            crime_type=crime_type_name,
            district=district_name,
            status="active" if row["status"] != "closed" else "closed",
            priority=row["priority"],
            officer_id=user.id if user else None,
            fir_id=fir.id if fir else None,
            incident_from_date=base + timedelta(days=i),
            incident_to_date=base + timedelta(days=i, hours=2),
            info_received_ps_date=base + timedelta(days=i, hours=3),
            case_category_id=category.id if category else None,
            gravity_offence_id=gravity.id if gravity else None,
            crime_major_head_id=head.id if head else None,
            crime_minor_head_id=sub.id if sub else None,
            case_status_id=case_status.id if case_status else None,
            court_id=court.id if court else None,
            police_person_id=officer.id if officer else None,
            police_station_id=station.id if station else None,
            latitude=12.97 + (i * 0.01) % 1,
            longitude=77.59 + (i * 0.01) % 1,
        ))
        n += 1

    await db.flush()
    return n
