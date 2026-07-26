from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
import httpx
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.crime import Crime
from app.core.response import success_response
from app.core.service_urls import get_ai_services_url
from app.db.phase1_store import using_phase1_store

router = APIRouter()


class CrossDistrictRequest(BaseModel):
    query: str
    districts: Optional[List[str]] = None
    crime_type: Optional[str] = None
    status: Optional[str] = None
    limit: int = 20


@router.post("")
async def cross_district_search(data: CrossDistrictRequest, db: AsyncSession = Depends(get_db)):
    from app.models.district import District

    if using_phase1_store():
        from app.db.phase1_aggregations import geo_context

        ctx = await geo_context()
        wanted = {d.strip().lower() for d in (data.districts or []) if d.strip()}
        query = (data.query or "").strip().lower()
        results = []
        for crime in ctx["crimes"]:
            district_name = ctx["district_names"].get(str(crime.get("district_id") or ""), "")
            if wanted and not any(w in district_name.lower() for w in wanted):
                continue
            if query and query not in str(crime.get("title") or "").lower():
                continue
            if data.status and str(crime.get("status") or "") != data.status:
                continue
            results.append({
                "id": crime.get("id"),
                "title": crime.get("title"),
                "district": district_name,
                "district_id": crime.get("district_id"),
                "status": crime.get("status"),
                "priority": crime.get("priority"),
                "created_at": str(crime.get("occurred_at") or ""),
                "entity": "crime",
            })
        results.sort(key=lambda x: x.get("created_at") or "", reverse=True)
        return success_response(data={
            "results": results[: data.limit],
            "total": len(results),
            "districts_searched": sorted(set(ctx["district_names"].values())) if not wanted else list(wanted),
        })

    if not data.districts:
        result = await db.execute(select(District))
        districts = [d.name for d in result.scalars().all()]
    else:
        districts = data.districts

    all_results = []

    for district_name in districts:
        district_result = await db.execute(
            select(District).where(District.name.ilike(f"%{district_name}%"))
        )
        district = district_result.scalar_one_or_none()
        if not district:
            continue

        crime_query = select(Crime).where(Crime.district_id == district.id)

        if data.query:
            crime_query = crime_query.where(
                or_(
                    Crime.title.ilike(f"%{data.query}%"),
                    Crime.description.ilike(f"%{data.query}%"),
                )
            )
        if data.status:
            crime_query = crime_query.where(Crime.status == data.status)

        crime_result = await db.execute(crime_query.limit(data.limit))
        crimes = crime_result.scalars().all()

        for crime in crimes:
            all_results.append({
                "id": crime.id,
                "title": crime.title,
                "district": district.name,
                "district_id": district.id,
                "status": crime.status,
                "priority": crime.priority,
                "created_at": str(crime.created_at) if crime.created_at else None,
                "entity": "crime",
            })

    all_results.sort(key=lambda x: x.get("created_at", ""), reverse=True)

    return success_response(data={
        "results": all_results[:data.limit],
        "total": len(all_results),
        "districts_searched": districts,
    })


@router.get("/districts")
async def list_districts(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all_safe

        rows = await fetch_all_safe("districts")
        return success_response(data=[
            {
                "id": d.get("id"),
                "name": d.get("name"),
                "code": d.get("code"),
                "state": d.get("state"),
                "population": d.get("population"),
            }
            for d in rows
        ])
    from app.models.district import District
    result = await db.execute(select(District))
    districts = [{"id": d.id, "name": d.name, "code": d.code} for d in result.scalars().all()]
    return success_response(data=districts)


@router.get("/stats/{district_name}")
async def district_stats(district_name: str, db: AsyncSession = Depends(get_db)):
    from app.models.district import District
    from app.models.crime import Crime as CrimeModel
    from sqlalchemy import func

    if using_phase1_store():
        from app.db.phase1_aggregations import geo_context

        ctx = await geo_context()
        needle = district_name.strip().lower()
        match = next(
            (d for d in ctx["districts"] if needle in str(d.get("name") or "").lower()),
            None,
        )
        if not match:
            return success_response(data={"error": "District not found"})
        crimes = [
            c
            for c in ctx["crimes"]
            if str(c.get("district_id")) in {str(match.get("id")), str(match.get("legacy_id"))}
        ]
        status_dist: dict[str, int] = {}
        for crime in crimes:
            key = str(crime.get("status") or "unknown")
            status_dist[key] = status_dist.get(key, 0) + 1
        return success_response(data={
            "district": match.get("name"),
            "code": match.get("code"),
            "total_crimes": len(crimes),
            "status_distribution": status_dist,
        })

    district_result = await db.execute(
        select(District).where(District.name.ilike(f"%{district_name}%"))
    )
    district = district_result.scalar_one_or_none()
    if not district:
        return success_response(data={"error": "District not found"})

    crime_count = (await db.execute(
        select(func.count(CrimeModel.id)).where(CrimeModel.district_id == district.id)
    )).scalar()

    status_result = await db.execute(
        select(CrimeModel.status, func.count(CrimeModel.id))
        .where(CrimeModel.district_id == district.id)
        .group_by(CrimeModel.status)
    )
    status_dist = {row[0]: row[1] for row in status_result.all()}

    return success_response(data={
        "district": district.name,
        "code": district.code,
        "total_crimes": crime_count,
        "status_distribution": status_dist,
    })
