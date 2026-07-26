from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.behavior_service import BehaviorService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return BehaviorService(db)


async def _phase1_profiles():
    from app.db.phase1_aggregations import derive_behavior_profiles, fetch_all_safe

    criminals = await fetch_all_safe("criminals")
    persons = await fetch_all_safe("persons")
    person_names = {}
    for person in persons:
        label = f"{person.get('first_name') or ''} {person.get('last_name') or ''}".strip()
        for key in ("id", "legacy_id"):
            if person.get(key) is not None:
                person_names.setdefault(str(person[key]), label)
    return derive_behavior_profiles(criminals, person_names)


@router.get("/stats")
async def behavior_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import behavior_stats as build_stats

        return success_response(data=build_stats(await _phase1_profiles()))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/profiles")
async def list_profiles(
    criminal_id: int = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        profiles = await _phase1_profiles()
        if criminal_id:
            profiles = [p for p in profiles if str(p["criminal_id"]) == str(criminal_id)]
        return success_response(data={"items": profiles, "total": len(profiles)})
    svc = get_service(db)
    profiles = await svc.get_profiles(criminal_id)
    return success_response(data={"items": profiles, "total": len(profiles)})


@router.post("/analyze/{criminal_id}")
async def analyze_criminal(criminal_id: int, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        profiles = [p for p in await _phase1_profiles() if str(p["criminal_id"]) == str(criminal_id)]
        if not profiles:
            return success_response(message="Criminal not found")
        return success_response(
            data={
                "criminal_id": criminal_id,
                "profiles_created": len(profiles),
                "profiles": profiles,
                "risk_level": profiles[0]["risk_level"],
                "risk_score": profiles[0]["risk_score"],
            },
            message="Behavioral profile generated",
        )
    svc = get_service(db)
    result = await svc.analyze_criminal(criminal_id)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Behavioral profile generated")


@router.get("/risk-assessment")
async def risk_assessment(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import behavior_risk_assessment

        return success_response(data=behavior_risk_assessment(await _phase1_profiles()))
    svc = get_service(db)
    return success_response(data=await svc.get_risk_assessment())


@router.get("/features/{profile_id}")
async def get_features(profile_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        match = next((p for p in await _phase1_profiles() if str(p["id"]) == str(profile_id)), None)
        features = (
            [
                {
                    "id": f"{profile_id}-{name}",
                    "feature_name": name,
                    "feature_value": value,
                    "weight": weight,
                }
                for name, value, weight in (
                    ("profile_type", match["profile_type"], 1.0),
                    ("confidence", str(match["confidence"]), 0.8),
                    ("risk_level", match["risk_level"], 0.9),
                )
            ]
            if match
            else []
        )
        return success_response(data={"items": features, "total": len(features)})
    if not profile_id.isdigit():
        return success_response(data={"items": [], "total": 0})
    svc = get_service(db)
    features = await svc.get_features(int(profile_id))
    return success_response(data={"items": features, "total": len(features)})
