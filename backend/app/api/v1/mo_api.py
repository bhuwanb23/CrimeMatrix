from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.mo_service import MOService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


class MOCompareRequest(BaseModel):
    profile_id_1: str
    profile_id_2: str


def get_service(db: AsyncSession):
    return MOService(db)


async def _phase1_mo_profiles():
    from app.db.phase1_aggregations import derive_mo_profiles, geo_context

    return derive_mo_profiles(await geo_context())


def _fingerprint_similarity(first: dict, second: dict) -> float:
    keys = set(first["fingerprint"]) | set(second["fingerprint"])
    if not keys:
        return 0.0
    shared = sum(1 for k in keys if first["fingerprint"].get(k) == second["fingerprint"].get(k))
    return round(shared / len(keys) * 100, 1)


@router.get("/stats")
async def mo_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import mo_stats as build_stats

        return success_response(data=build_stats(await _phase1_mo_profiles()))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/profiles")
async def list_profiles(
    crime_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        profiles = await _phase1_mo_profiles()
        if crime_id:
            profiles = [p for p in profiles if str(p["crime_id"]) == str(crime_id)]
        return success_response(data={"items": profiles, "total": len(profiles)})
    svc = get_service(db)
    profiles = await svc.get_profiles(crime_id)
    return success_response(data={"items": profiles, "total": len(profiles)})


@router.get("/profiles/{profile_id}")
async def get_profile(profile_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        match = next(
            (p for p in await _phase1_mo_profiles() if str(p["id"]) == str(profile_id)), None
        )
        if not match:
            return success_response(message="Profile not found")
        return success_response(data=match)
    if not profile_id.isdigit():
        return success_response(message="Profile not found")
    svc = get_service(db)
    profile = await svc.get_profile(int(profile_id))
    if not profile:
        return success_response(message="Profile not found")
    return success_response(data=profile)


@router.post("/fingerprint/{crime_id}")
async def create_fingerprint(crime_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        match = next(
            (p for p in await _phase1_mo_profiles() if str(p["crime_id"]) == str(crime_id)), None
        )
        if not match:
            return success_response(message="Crime not found")
        return success_response(data=match, message="MO fingerprint created")
    svc = get_service(db)
    result = await svc.create_fingerprint(crime_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="MO fingerprint created")


@router.post("/compare")
async def compare_profiles(data: MOCompareRequest, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        by_id = {str(p["id"]): p for p in await _phase1_mo_profiles()}
        first, second = by_id.get(str(data.profile_id_1)), by_id.get(str(data.profile_id_2))
        if not first or not second:
            return success_response(message="Profile not found")
        return success_response(data={
            "profile_1": first,
            "profile_2": second,
            "similarity_score": _fingerprint_similarity(first, second),
            "shared_features": [
                key
                for key in first["fingerprint"]
                if first["fingerprint"].get(key) == second["fingerprint"].get(key)
            ],
        })
    svc = get_service(db)
    if not (str(data.profile_id_1).isdigit() and str(data.profile_id_2).isdigit()):
        return success_response(message="Profile not found")
    result = await svc.compare_profiles(int(data.profile_id_1), int(data.profile_id_2))
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)


@router.get("/similar/{profile_id}")
async def find_similar(
    profile_id: str,
    top_k: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        profiles = await _phase1_mo_profiles()
        target = next((p for p in profiles if str(p["id"]) == str(profile_id)), None)
        if not target:
            return success_response(data={"items": [], "total": 0})
        scored = [
            {
                "profile_id": p["id"],
                "crime_id": p["crime_id"],
                "title": p["title"],
                "similarity_score": _fingerprint_similarity(target, p),
                "mo_text": p["mo_text"],
            }
            for p in profiles
            if str(p["id"]) != str(profile_id)
        ]
        scored.sort(key=lambda s: s["similarity_score"], reverse=True)
        items = scored[:top_k]
        return success_response(data={"items": items, "total": len(items)})
    if not profile_id.isdigit():
        return success_response(data={"items": [], "total": 0})
    svc = get_service(db)
    similar = await svc.find_similar(int(profile_id), top_k)
    return success_response(data={"items": similar, "total": len(similar)})


@router.post("/batch-fingerprint")
async def batch_fingerprint(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import mo_stats as build_stats

        profiles = await _phase1_mo_profiles()
        return success_response(
            data={"profiles_created": len(profiles), **build_stats(profiles)},
            message="Batch fingerprinting complete",
        )
    svc = get_service(db)
    result = await svc.batch_fingerprint()
    return success_response(data=result, message="Batch fingerprinting complete")
