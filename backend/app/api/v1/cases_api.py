from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.session import get_db
from app.repositories.case_repo import CaseRepository
from app.services.case_service import CaseService
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse
from app.schemas.complainant import ComplainantCreate, ComplainantUpdate, ComplainantResponse
from app.core.response import success_response
from sqlalchemy import select
from app.models.complainant import Complainant
from app.models.occupation import Occupation
from app.models.religion import Religion
from app.models.caste_master import CasteMaster
from app.models.gender import Gender
from app.models.act import Act
from app.models.section import Section
from app.models.act_section_association import ActSectionAssociation
from app.models.victim import Victim
from pydantic import BaseModel

router = APIRouter()


def get_service(db: AsyncSession):
    return CaseService(CaseRepository(db))


@router.get("/")
async def list_cases(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    district: Optional[str] = None,
    status: Optional[str] = None,
    crime_type: Optional[str] = None,
    case_category_id: Optional[int] = None,
    police_station_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    if district:
        cases = await svc.get_by_district(district)
    elif status:
        cases = await svc.get_by_status(status)
    elif case_category_id:
        cases = await svc.repo.get_by_category(case_category_id)
    elif police_station_id:
        cases = await svc.repo.get_by_station(police_station_id)
    else:
        from app.schemas.common import PaginationParams
        params = PaginationParams(page=page, page_size=page_size)
        result = await svc.get_paginated(params)
        return success_response(data={
            "items": [CaseResponse.model_validate(c).model_dump() for c in result.items],
            "total": result.total,
            "page": result.page,
            "page_size": result.page_size,
            "total_pages": result.total_pages,
        })

    start = (page - 1) * page_size
    paginated = cases[start:start + page_size]
    return success_response(data={
        "items": [CaseResponse.model_validate(c).model_dump() for c in paginated],
        "total": len(cases),
        "page": page,
        "page_size": page_size,
        "total_pages": (len(cases) + page_size - 1) // page_size,
    })


@router.get("/{case_id}")
async def get_case(case_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.get_by_id(case_id)
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump())


@router.get("/by-number/{case_number}")
async def get_case_by_number(case_number: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.get_by_number(case_number)
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump())


@router.get("/by-crime-no/{crime_no}")
async def get_case_by_crime_no(crime_no: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.repo.get_by_crime_no(crime_no)
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump())


@router.post("/")
async def create_case(data: CaseCreate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.create(data.model_dump(exclude_unset=True))
    return success_response(data=CaseResponse.model_validate(case).model_dump(), message="Case created")


@router.put("/{case_id}")
async def update_case(case_id: int, data: CaseUpdate, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    case = await svc.update(case_id, data.model_dump(exclude_unset=True))
    if not case:
        return success_response(message="Case not found")
    return success_response(data=CaseResponse.model_validate(case).model_dump(), message="Case updated")


@router.delete("/{case_id}")
async def delete_case(case_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    deleted = await svc.delete(case_id)
    return success_response(message="Case deleted" if deleted else "Case not found")


@router.get("/search/{query}")
async def search_cases(query: str, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    results = await svc.search_cases(query)
    return success_response(data=[CaseResponse.model_validate(r).model_dump() for r in results])


# --- Complainant Endpoints ---

async def _enrich_complainant(c, db):
    data = ComplainantResponse.model_validate(c).model_dump()
    if c.occupation_id:
        occ = (await db.execute(select(Occupation).where(Occupation.id == c.occupation_id))).scalar()
        data["occupation_name"] = occ.name if occ else None
    if c.religion_id:
        rel = (await db.execute(select(Religion).where(Religion.id == c.religion_id))).scalar()
        data["religion_name"] = rel.name if rel else None
    if c.caste_id:
        caste = (await db.execute(select(CasteMaster).where(CasteMaster.id == c.caste_id))).scalar()
        data["caste_name"] = caste.name if caste else None
    if c.gender_id:
        gen = (await db.execute(select(Gender).where(Gender.id == c.gender_id))).scalar()
        data["gender_name"] = gen.name if gen else None
    return data


@router.get("/{case_id}/complainant")
async def get_complainant(case_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Complainant).where(Complainant.case_id == case_id))
    c = result.scalar()
    if not c:
        return success_response(message="No complainant found for this case")
    data = await _enrich_complainant(c, db)
    return success_response(data=data)


@router.post("/{case_id}/complainant")
async def create_complainant(case_id: int, data: ComplainantCreate, db: AsyncSession = Depends(get_db)):
    existing = (await db.execute(select(Complainant).where(Complainant.case_id == case_id))).scalar()
    if existing:
        return success_response(message="Complainant already exists for this case. Use PUT to update.")
    c = Complainant(case_id=case_id, name=data.name, age_year=data.age_year,
                    occupation_id=data.occupation_id, religion_id=data.religion_id,
                    caste_id=data.caste_id, gender_id=data.gender_id)
    db.add(c)
    await db.commit()
    await db.refresh(c)
    enriched = await _enrich_complainant(c, db)
    return success_response(data=enriched, message="Complainant created")


@router.put("/{case_id}/complainant")
async def update_complainant(case_id: int, data: ComplainantUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Complainant).where(Complainant.case_id == case_id))
    c = result.scalar()
    if not c:
        return success_response(message="No complainant found for this case")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(c, key, value)
    await db.commit()
    await db.refresh(c)
    enriched = await _enrich_complainant(c, db)
    return success_response(data=enriched, message="Complainant updated")


@router.delete("/{case_id}/complainant")
async def delete_complainant(case_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Complainant).where(Complainant.case_id == case_id))
    c = result.scalar()
    if not c:
        return success_response(message="No complainant found")
    await db.delete(c)
    await db.commit()
    return success_response(message="Complainant deleted")


# --- ActSection Schemas ---
class ActSectionCreate(BaseModel):
    act_id: int
    section_id: int
    act_order: int = 1
    section_order: int = 1


# --- ActSection Endpoints ---

@router.get("/{case_id}/act-sections")
async def get_act_sections(case_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActSectionAssociation).where(ActSectionAssociation.case_id == case_id).order_by(ActSectionAssociation.act_order))
    items = []
    for a in result.scalars().all():
        act = (await db.execute(select(Act).where(Act.id == a.act_id))).scalar()
        sec = (await db.execute(select(Section).where(Section.id == a.section_id))).scalar()
        items.append({
            "id": a.id, "case_id": a.case_id,
            "act_id": a.act_id, "act_name": act.name if act else None, "act_code": act.act_code if act else None,
            "section_id": a.section_id, "section_name": sec.name if sec else None, "section_code": sec.section_code if sec else None,
            "act_order": a.act_order, "section_order": a.section_order,
        })
    return success_response(data={"items": items, "total": len(items)})


@router.post("/{case_id}/act-sections")
async def add_act_section(case_id: int, data: ActSectionCreate, db: AsyncSession = Depends(get_db)):
    a = ActSectionAssociation(case_id=case_id, act_id=data.act_id, section_id=data.section_id,
                               act_order=data.act_order, section_order=data.section_order)
    db.add(a)
    await db.commit()
    await db.refresh(a)
    return success_response(data={"id": a.id, "case_id": a.case_id}, message="Act-Section added")


@router.delete("/{case_id}/act-sections/{assoc_id}")
async def delete_act_section(case_id: int, assoc_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ActSectionAssociation).where(ActSectionAssociation.id == assoc_id, ActSectionAssociation.case_id == case_id))
    a = result.scalar()
    if not a:
        return success_response(message="Not found")
    await db.delete(a)
    await db.commit()
    return success_response(message="Deleted")


# --- Victim Schemas ---
class VictimCreate(BaseModel):
    name: str
    age_year: Optional[int] = None
    gender_id: Optional[int] = None
    is_police: bool = False


class VictimUpdate(BaseModel):
    name: Optional[str] = None
    age_year: Optional[int] = None
    gender_id: Optional[int] = None
    is_police: Optional[bool] = None


# --- Victim Endpoints ---

@router.get("/{case_id}/victims")
async def get_victims(case_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Victim).where(Victim.case_id == case_id))
    items = []
    for v in result.scalars().all():
        gen = (await db.execute(select(Gender).where(Gender.id == v.gender_id))).scalar() if v.gender_id else None
        items.append({
            "id": v.id, "case_id": v.case_id, "name": v.name,
            "age_year": v.age_year, "gender_id": v.gender_id,
            "gender_name": gen.name if gen else None,
            "is_police": v.is_police,
            "created_at": str(v.created_at) if v.created_at else None,
        })
    return success_response(data={"items": items, "total": len(items)})


@router.post("/{case_id}/victims")
async def create_victim(case_id: int, data: VictimCreate, db: AsyncSession = Depends(get_db)):
    v = Victim(case_id=case_id, name=data.name, age_year=data.age_year,
               gender_id=data.gender_id, is_police=data.is_police)
    db.add(v)
    await db.commit()
    await db.refresh(v)
    gen = (await db.execute(select(Gender).where(Gender.id == v.gender_id))).scalar() if v.gender_id else None
    return success_response(data={
        "id": v.id, "case_id": v.case_id, "name": v.name,
        "age_year": v.age_year, "gender_id": v.gender_id,
        "gender_name": gen.name if gen else None, "is_police": v.is_police,
    }, message="Victim created")


@router.put("/{case_id}/victims/{victim_id}")
async def update_victim(case_id: int, victim_id: int, data: VictimUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Victim).where(Victim.id == victim_id, Victim.case_id == case_id))
    v = result.scalar()
    if not v:
        return success_response(message="Victim not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(v, key, value)
    await db.commit()
    await db.refresh(v)
    gen = (await db.execute(select(Gender).where(Gender.id == v.gender_id))).scalar() if v.gender_id else None
    return success_response(data={
        "id": v.id, "case_id": v.case_id, "name": v.name,
        "age_year": v.age_year, "gender_id": v.gender_id,
        "gender_name": gen.name if gen else None, "is_police": v.is_police,
    }, message="Victim updated")


@router.delete("/{case_id}/victims/{victim_id}")
async def delete_victim(case_id: int, victim_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Victim).where(Victim.id == victim_id, Victim.case_id == case_id))
    v = result.scalar()
    if not v:
        return success_response(message="Victim not found")
    await db.delete(v)
    await db.commit()
    return success_response(message="Victim deleted")
