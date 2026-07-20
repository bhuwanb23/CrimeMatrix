from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.mo_service import MOService
from app.core.response import success_response

router = APIRouter()


class MOCompareRequest(BaseModel):
    profile_id_1: int
    profile_id_2: int


def get_service(db: AsyncSession):
    return MOService(db)


@router.get("/stats")
async def mo_stats(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/profiles")
async def list_profiles(
    crime_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    profiles = await svc.get_profiles(crime_id)
    return success_response(data={"items": profiles, "total": len(profiles)})


@router.get("/profiles/{profile_id}")
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    profile = await svc.get_profile(profile_id)
    if not profile:
        return success_response(message="Profile not found")
    return success_response(data=profile)


@router.post("/fingerprint/{crime_id}")
async def create_fingerprint(crime_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.create_fingerprint(crime_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="MO fingerprint created")


@router.post("/compare")
async def compare_profiles(data: MOCompareRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.compare_profiles(data.profile_id_1, data.profile_id_2)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)


@router.get("/similar/{profile_id}")
async def find_similar(
    profile_id: int,
    top_k: int = Query(default=5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    similar = await svc.find_similar(profile_id, top_k)
    return success_response(data={"items": similar, "total": len(similar)})


@router.post("/batch-fingerprint")
async def batch_fingerprint(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.batch_fingerprint()
    return success_response(data=result, message="Batch fingerprinting complete")
