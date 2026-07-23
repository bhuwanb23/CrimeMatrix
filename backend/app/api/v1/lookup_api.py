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
from app.models.occupation import Occupation
from app.models.religion import Religion
from app.models.caste_master import CasteMaster
from app.models.gender import Gender
from app.models.act import Act
from app.models.section import Section
from app.models.state import State
from app.models.arrest_surrender_type import ArrestSurrenderType
from app.models.crime_head_act_section import CrimeHeadActSection
from app.models.unit_type import UnitType
from app.models.rank import Rank

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


@router.get("/occupations")
async def list_occupations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Occupation).order_by(Occupation.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/religions")
async def list_religions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Religion).order_by(Religion.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/caste")
async def list_caste(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CasteMaster).order_by(CasteMaster.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/genders")
async def list_genders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Gender).order_by(Gender.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/acts")
async def list_acts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Act).order_by(Act.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "act_code": r.act_code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/sections")
async def list_sections(act_id: int = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Section)
    if act_id:
        stmt = stmt.where(Section.act_id == act_id)
    result = await db.execute(stmt.order_by(Section.section_code))
    items = [{"id": r.id, "name": r.name, "code": r.code, "section_code": r.section_code, "act_id": r.act_id, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/states")
async def list_states(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(State).order_by(State.name))
    items = [{"id": r.id, "name": r.name, "code": r.code} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/arrest-surrender-types")
async def list_arrest_surrender_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ArrestSurrenderType).order_by(ArrestSurrenderType.name))
    items = [{"id": r.id, "name": r.name, "code": r.code, "description": r.description} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/crime-head-act-sections")
async def list_crime_head_act_sections(crime_head_id: int = None, db: AsyncSession = Depends(get_db)):
    stmt = select(CrimeHeadActSection)
    if crime_head_id:
        stmt = stmt.where(CrimeHeadActSection.crime_head_id == crime_head_id)
    result = await db.execute(stmt)
    items = []
    for r in result.scalars().all():
        head = (await db.execute(select(CrimeHead).where(CrimeHead.id == r.crime_head_id))).scalar()
        act = (await db.execute(select(Act).where(Act.act_code == r.act_code))).scalar()
        items.append({
            "id": r.id, "crime_head_id": r.crime_head_id,
            "crime_head_name": head.name if head else None,
            "act_code": r.act_code, "act_name": act.name if act else None,
            "section_code": r.section_code,
        })
    return success_response(data={"items": items, "total": len(items)})


@router.get("/unit-types")
async def list_unit_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UnitType).order_by(UnitType.hierarchy))
    items = [{"id": r.id, "name": r.name, "code": r.code, "city_dist_state": r.city_dist_state, "hierarchy": r.hierarchy, "active": r.active} for r in result.scalars().all()]
    return success_response(data={"items": items, "total": len(items)})


@router.get("/ranks")
async def list_ranks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rank).order_by(Rank.hierarchy))
    items = [{"id": r.id, "name": r.name, "code": r.code, "hierarchy": r.hierarchy, "active": r.active} for r in result.scalars().all()]
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

    # Occupations
    occupations_data = [
        ("Government Employee", "GOV", "Central or state government employee"),
        ("Private Employee", "PVT", "Private sector employee"),
        ("Business", "BIZ", "Business owner or self-employed"),
        ("Student", "STD", "Student"),
        ("Farmer", "FAR", "Agricultural worker or farmer"),
        ("Daily Wage Worker", "DWG", "Daily wage laborer"),
        ("Professional", "PRF", "Doctor, lawyer, engineer, etc."),
        ("Retired", "RET", "Retired person"),
        ("Unemployed", "UNEMP", "Currently unemployed"),
        ("Homemaker", "HOME", "Homemaker"),
        ("Driver", "DRV", "Driver (taxi, truck, auto)"),
        ("Housewife", "HSW", "Housewife"),
    ]
    for name, code, desc in occupations_data:
        exists = await db.execute(select(Occupation).where(Occupation.code == code))
        if not exists.scalar():
            db.add(Occupation(name=name, code=code, description=desc))
            seeded += 1

    # Religions
    religions_data = [
        ("Hindu", "HIN", "Hinduism"),
        ("Muslim", "MUS", "Islam"),
        ("Christian", "CHR", "Christianity"),
        ("Sikh", "SIK", "Sikhism"),
        ("Buddhist", "BUD", "Buddhism"),
        ("Jain", "JAI", "Jainism"),
        ("Other", "OTH", "Other religion"),
        ("Not Specified", "NS", "Religion not specified"),
    ]
    for name, code, desc in religions_data:
        exists = await db.execute(select(Religion).where(Religion.code == code))
        if not exists.scalar():
            db.add(Religion(name=name, code=code, description=desc))
            seeded += 1

    # Caste
    caste_data = [
        ("General", "GEN", "General category"),
        ("SC", "SC", "Scheduled Caste"),
        ("ST", "ST", "Scheduled Tribe"),
        ("OBC", "OBC", "Other Backward Classes"),
        ("EWS", "EWS", "Economically Weaker Section"),
        ("Other", "OTH", "Other caste"),
        ("Not Specified", "NS", "Caste not specified"),
    ]
    for name, code, desc in caste_data:
        exists = await db.execute(select(CasteMaster).where(CasteMaster.code == code))
        if not exists.scalar():
            db.add(CasteMaster(name=name, code=code, description=desc))
            seeded += 1

    # Genders
    genders_data = [
        ("Male", "M", "Male"),
        ("Female", "F", "Female"),
        ("Transgender", "T", "Transgender"),
        ("Other", "O", "Other gender"),
        ("Not Specified", "NS", "Gender not specified"),
    ]
    for name, code, desc in genders_data:
        exists = await db.execute(select(Gender).where(Gender.code == code))
        if not exists.scalar():
            db.add(Gender(name=name, code=code, description=desc))
            seeded += 1

    # Acts
    acts_data = [
        ("Indian Penal Code", "IPC", "IPC", "Indian Penal Code, 1860"),
        ("Bharatiya Nyaya Sanhita", "BNS", "BNS", "Bharatiya Nyaya Sanhita, 2023"),
        ("Code of Criminal Procedure", "CrPC", "CrPC", "Code of Criminal Procedure, 1973"),
        ("Indian Evidence Act", "IEA", "IEA", "Indian Evidence Act, 1872"),
        ("Narcotic Drugs and Psychotropic Substances Act", "NDPS", "NDPS", "NDPS Act, 1985"),
        ("Information Technology Act", "ITA", "ITA", "Information Technology Act, 2000"),
        ("Arms Act", "ARM", "ARM", "Arms Act, 1959"),
        ("Protection of Children from Sexual Offences Act", "POCSO", "POCSO", "POCSO Act, 2012"),
        ("Dowry Prohibition Act", "DPA", "DPA", "Dowry Prohibition Act, 1961"),
        ("Motor Vehicles Act", "MVA", "MVA", "Motor Vehicles Act, 1988"),
        ("Excise Act", "EXC", "EXC", "Karnataka Excise Act"),
        ("Prevention of Corruption Act", "PCA", "PCA", "Prevention of Corruption Act, 1988"),
    ]
    for name, code, act_code, desc in acts_data:
        exists = await db.execute(select(Act).where(Act.act_code == act_code))
        if not exists.scalar():
            db.add(Act(name=name, code=code, act_code=act_code, short_name=code, description=desc, active=True))
            seeded += 1

    # Sections (key IPC sections)
    sections_data = [
        ("Murder", "302", "IPC", 1),
        ("Attempt to Murder", "307", "IPC", 1),
        ("Culpable Homicide", "304", "IPC", 1),
        ("Robbery", "392", "IPC", 1),
        ("Dacoity", "395", "IPC", 1),
        ("Theft", "379", "IPC", 1),
        ("Burglary", "454", "IPC", 1),
        ("Cheating", "420", "IPC", 1),
        ("Criminal Intimidation", "506", "IPC", 1),
        ("Assault", "323", "IPC", 1),
        ("Kidnapping", "363", "IPC", 1),
        ("Rape", "376", "IPC", 1),
        ("Dowry Death", "304B", "IPC", 1),
        ("Cruelty by Husband", "498A", "IPC", 1),
        ("Arson", "435", "IPC", 1),
        ("Criminal Breach of Trust", "406", "IPC", 1),
        ("Forging Documents", "465", "IPC", 1),
        ("Hacking", "66", "ITA", 6),
        ("Drug Trafficking", "20", "NDPS", 5),
        ("Drug Possession", "8", "NDPS", 5),
        ("Arms Possession", "25", "ARM", 7),
        ("POCSO Offence", "4", "POCSO", 8),
        ("Dowry Harassment", "498A", "IPC", 1),
        ("Stalking", "354D", "IPC", 1),
        ("Outraging Modesty", "354", "IPC", 1),
    ]
    for name, section_code, act_code, act_id in sections_data:
        exists = await db.execute(select(Section).where(Section.section_code == section_code).where(Section.act_id == act_id))
        if not exists.scalar():
            db.add(Section(name=name, code=section_code, section_code=section_code, act_id=act_id, description=f"Section {section_code}", active=True))
            seeded += 1

    # States
    states_data = [
        ("Karnataka", "KA"),
        ("Maharashtra", "MH"),
        ("Tamil Nadu", "TN"),
        ("Kerala", "KL"),
        ("Andhra Pradesh", "AP"),
        ("Telangana", "TS"),
        ("Goa", "GA"),
        ("Puducherry", "PY"),
    ]
    for name, code in states_data:
        exists = await db.execute(select(State).where(State.code == code))
        if not exists.scalar():
            db.add(State(name=name, code=code))
            seeded += 1

    # Arrest/Surrender Types
    arrest_types = [
        ("Arrest", "ARR", "Person arrested by police"),
        ("Voluntary Surrender", "SUR", "Voluntary surrender before police or court"),
        ("Surrender in Court", "SCT", "Surrender before court"),
    ]
    for name, code, desc in arrest_types:
        exists = await db.execute(select(ArrestSurrenderType).where(ArrestSurrenderType.code == code))
        if not exists.scalar():
            db.add(ArrestSurrenderType(name=name, code=code, description=desc))
            seeded += 1

    # Unit Types
    unit_types_data = [
        ("Police Station", "PS", "City", 4, "Local police station"),
        ("Circle Office", "CO", "District", 3, "Circle-level police office"),
        ("Sub-Division", "SD", "District", 2, "Sub-divisional police office"),
        ("District Police", "DP", "District", 1, "District police headquarters"),
        ("Commissionerate", "CMP", "City", 1, "City police commissionerate"),
        ("State Headquarters", "SHQ", "State", 0, "State police headquarters"),
    ]
    for name, code, cds, hierarchy, desc in unit_types_data:
        exists = await db.execute(select(UnitType).where(UnitType.code == code))
        if not exists.scalar():
            db.add(UnitType(name=name, code=code, city_dist_state=cds, hierarchy=hierarchy, description=desc, active=True))
            seeded += 1

    # Ranks
    ranks_data = [
        ("Constable", "CON", 10, "Entry-level police constable"),
        ("Head Constable", "HC", 9, "Senior constable"),
        ("Assistant Sub-Inspector", "ASI", 8, "Assistant sub-inspector"),
        ("Sub-Inspector", "SI", 7, "Sub-inspector"),
        ("Inspector", "INS", 6, "Police inspector"),
        ("Deputy Superintendent of Police", "DSP", 5, "Deputy SP"),
        ("Superintendent of Police", "SP", 4, "District SP"),
        ("Deputy Inspector General", "DIG", 3, "Deputy Inspector General"),
        ("Inspector General", "IG", 2, "Inspector General"),
        ("Director General of Police", "DGP", 1, "State DGP"),
    ]
    for name, code, hierarchy, desc in ranks_data:
        exists = await db.execute(select(Rank).where(Rank.code == code))
        if not exists.scalar():
            db.add(Rank(name=name, code=code, hierarchy=hierarchy, description=desc, active=True))
            seeded += 1

    await db.commit()
    return success_response(data={"seeded": seeded}, message=f"Seeded {seeded} lookup records")
