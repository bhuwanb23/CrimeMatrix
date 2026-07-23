from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.response import success_response
from app.models.case_category import CaseCategory
from app.models.gravity_offence import GravityOffence
from app.models.crime_head import CrimeHead
from app.models.crime_sub_head import CrimeSubHead
from app.models.case_status_master import CaseStatusMaster
from app.models.court import Court

router = APIRouter()


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CaseCategory).order_by(CaseCategory.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/gravity-offences")
async def list_gravity_offences(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GravityOffence).order_by(GravityOffence.severity_level))
    items = [{"id": r.id, "name": r.name, "code": r.code, "severity_level": r.severity_level, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/crime-heads")
async def list_crime_heads(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CrimeHead).order_by(CrimeHead.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/crime-sub-heads")
async def list_crime_sub_heads(crime_head_id: int = None, db: AsyncSession = Depends(get_db)):
    stmt = select(CrimeSubHead)
    if crime_head_id:
        stmt = stmt.where(CrimeSubHead.crime_head_id == crime_head_id)
    result = await db.execute(stmt.order_by(CrimeSubHead.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "crime_head_id": r.crime_head_id, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/case-statuses")
async def list_case_statuses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CaseStatusMaster).order_by(CaseStatusMaster.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/courts")
async def list_courts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Court).order_by(Court.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "district": r.district, "court_type": r.court_type} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.post("/seed")
async def seed_lookups(db: AsyncSession = Depends(get_db)):
    seeded = 0

    # Case Categories
    cats = [
        ("FIR", "FIR", "First Information Report"),
        ("Zero FIR", "ZFIR", "Zero FIR — filed at any station"),
        ("UDR", "UDR", "Untraced Daily Report"),
        ("PAR", "PAR", "Prosecution Against Register"),
        ("NCR", "NCR", "Non-Cognizable Report"),
    ]
    for name, code, desc in cats:
        exists = await db.execute(select(CaseCategory).where(CaseCategory.code == code))
        if not exists.scalar():
            db.add(CaseCategory(name=name, code=code, description=desc))
            seeded += 1

    # Gravity Offences
    gravities = [
        ("Murder", "MUR", 10, "Section 302 IPC — Murder"),
        ("Rape", "RAP", 9, "Section 376 IPC — Rape"),
        ("Robbery", "ROB", 7, "Section 392 IPC — Robbery"),
        ("Dacoity", "DAC", 8, "Section 395 IPC — Dacoity"),
        ("Kidnapping", "KID", 7, "Section 363 IPC — Kidnapping"),
        ("Arson", "ARS", 6, "Section 435 IPC — Arson"),
        ("Assault", "ASS", 5, "Section 323 IPC — Assault"),
        ("Theft", "THF", 4, "Section 379 IPC — Theft"),
        ("Fraud", "FRD", 4, "Section 420 IPC — Cheating"),
        ("Cybercrime", "CYB", 5, "IT Act offences"),
        ("Drug Offence", "DRG", 6, "NDPS Act offences"),
        ("General", "GEN", 1, "General / non-gravity offence"),
    ]
    for name, code, sev, desc in gravities:
        exists = await db.execute(select(GravityOffence).where(GravityOffence.code == code))
        if not exists.scalar():
            db.add(GravityOffence(name=name, code=code, severity_level=sev, description=desc))
            seeded += 1

    # Crime Heads
    heads = [
        ("Offences Against Body", "OAB", "Crimes affecting person"),
        ("Offences Against Property", "OAP", "Crimes against property"),
        ("Offences Against Women", "OAW", "Crimes against women"),
        ("Offences Against Children", "OAC", "Crimes against children"),
        ("Economic Offences", "ECO", "Financial and economic crimes"),
        ("Cyber Offences", "CYO", "Technology-related crimes"),
        ("NDPS Offences", "NDP", "Narcotics offences"),
        ("Arms Act Offences", "ARM", "Weapons-related crimes"),
        ("Excise Offences", "EXC", "Liquor and excise crimes"),
        ("Other Offences", "OTH", "Miscellaneous offences"),
    ]
    for name, code, desc in heads:
        exists = await db.execute(select(CrimeHead).where(CrimeHead.code == code))
        if not exists.scalar():
            db.add(CrimeHead(name=name, code=code, description=desc))
            seeded += 1

    # Crime Sub Heads
    sub_heads = [
        ("Murder", "MUR", "OAB"), ("Attempt to Murder", "ATM", "OAB"),
        ("Culpable Homicide", "CHM", "OAB"), ("Assault", "AST", "OAB"),
        ("Kidnapping", "KID", "OAB"), ("Robbery", "ROB", "OAP"),
        ("Burglary", "BRG", "OAP"), ("Theft", "THF", "OAP"),
        ("Criminal Breach of Trust", "CBT", "OAP"),
        ("Rape", "RAP", "OAW"), ("Dowry Death", "DWD", "OAW"),
        ("Acid Attack", "ACD", "OAW"),
        ("Child Labour", "CHL", "OAC"), ("POCSO", "PCS", "OAC"),
        ("Cheating", "CHT", "ECO"), ("Forgery", "FRG", "ECO"),
        ("Money Laundering", "MLN", "ECO"),
        ("Hacking", "HCK", "CYO"), ("Identity Theft", "IDT", "CYO"),
        ("Drug Trafficking", "DTF", "NDP"), ("Drug Possession", "DPS", "NDP"),
        ("Arms Possession", "ARM", "ARM"), ("Unlawful Assembly", "ULA", "ARM"),
        ("Other", "OTH", "OTH"),
    ]
    for name, code, head_code in sub_heads:
        exists = await db.execute(select(CrimeSubHead).where(CrimeSubHead.code == code))
        if not exists.scalar():
            head_result = await db.execute(select(CrimeHead).where(CrimeHead.code == head_code))
            head = head_result.scalar()
            db.add(CrimeSubHead(name=name, code=code, crime_head_id=head.id if head else None))
            seeded += 1

    # Case Statuses
    statuses = [
        ("Registered", "REG", "FIR registered"),
        ("Under Investigation", "INV", "Case under active investigation"),
        ("Charge Sheet Filed", "CHS", "Charge sheet filed in court"),
        ("Convicted", "CONV", "Accused convicted"),
        ("Acquitted", "ACQ", "Accused acquitted"),
        ("Closed", "CLS", "Case closed"),
        ("Transfer Red", "XFR", "Case transferred to another station"),
        ("Abated", "ABT", "Case abated"),
    ]
    for name, code, desc in statuses:
        exists = await db.execute(select(CaseStatusMaster).where(CaseStatusMaster.code == code))
        if not exists.scalar():
            db.add(CaseStatusMaster(name=name, code=code, description=desc))
            seeded += 1

    # Courts
    courts_data = [
        ("Sessions Court Bengaluru", "SCBNG", "Bengaluru Urban", "Sessions"),
        ("Sessions Court Mysuru", "SCMYS", "Mysuru", "Sessions"),
        ("Sessions Court Mangaluru", "SCMNG", "Mangaluru", "Sessions"),
        ("JMFC Court Bengaluru", "JMBNG", "Bengaluru Urban", "JMFC"),
        ("JMFC Court Mysuru", "JMMYS", "Mysuru", "JMFC"),
        ("Special Court (NDPS) Bengaluru", "SCNDPS", "Bengaluru Urban", "Special"),
        ("Fast Track Court Bengaluru", "FTCBNG", "Bengaluru Urban", "Fast Track"),
        ("Family Court Bengaluru", "FCBNG", "Bengaluru Urban", "Family"),
    ]
    for name, code, district, ctype in courts_data:
        exists = await db.execute(select(Court).where(Court.code == code))
        if not exists.scalar():
            db.add(Court(name=name, code=code, district=district, court_type=ctype))
            seeded += 1

    await db.commit()
    return success_response(data={"seeded": seeded}, message=f"Seeded {seeded} lookup records")
