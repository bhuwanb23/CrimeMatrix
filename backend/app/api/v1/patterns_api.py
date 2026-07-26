from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.pattern_service import PatternService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


def get_service(db: AsyncSession):
    return PatternService(db)


async def _phase1_patterns():
    from app.db.phase1_aggregations import derive_patterns, geo_context

    ctx = await geo_context()
    return ctx, derive_patterns(ctx)


@router.get("/stats")
async def pattern_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import pattern_clusters
        from app.db.phase1_aggregations import pattern_stats as build_stats

        _, patterns = await _phase1_patterns()
        return success_response(data=build_stats(patterns, pattern_clusters(patterns)))
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/")
async def list_patterns(
    pattern_type: str = Query(default=None),
    crime_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        _, patterns = await _phase1_patterns()
        if pattern_type:
            patterns = [p for p in patterns if p["pattern_type"] == pattern_type]
        if crime_type:
            patterns = [p for p in patterns if p["crime_type"] == crime_type]
        return success_response(data={"items": patterns, "total": len(patterns)})
    svc = get_service(db)
    patterns = await svc.get_patterns(pattern_type=pattern_type, crime_type=crime_type)
    return success_response(data={"items": patterns, "total": len(patterns)})


@router.get("/clusters")
async def get_clusters(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import pattern_clusters

        _, patterns = await _phase1_patterns()
        return success_response(data=pattern_clusters(patterns))
    svc = get_service(db)
    clusters = await svc.get_clusters()
    return success_response(data=clusters)


@router.post("/detect")
async def detect_patterns(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import pattern_clusters

        ctx, patterns = await _phase1_patterns()
        clusters = pattern_clusters(patterns)
        return success_response(
            data={
                "patterns_found": len(patterns),
                "patterns_saved": len(patterns),
                "clusters_found": len(clusters),
                "total_crimes_analyzed": len(ctx["crimes"]),
                "items": patterns,
            },
            message="Pattern detection complete",
        )
    svc = get_service(db)
    result = await svc.detect_patterns()
    return success_response(data=result, message="Pattern detection complete")


@router.get("/compare/{p1_id}/{p2_id}")
async def compare_patterns(p1_id: str, p2_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        _, patterns = await _phase1_patterns()
        by_id = {str(p["id"]): p for p in patterns}
        first, second = by_id.get(str(p1_id)), by_id.get(str(p2_id))
        if not first or not second:
            return success_response(message="Pattern not found")
        shared = []
        if first["crime_type"] == second["crime_type"]:
            shared.append(f"Same crime type: {first['crime_type']}")
        if first["time_pattern"] == second["time_pattern"]:
            shared.append(f"Same time pattern: {first['time_pattern']}")
        if first["location_pattern"] == second["location_pattern"]:
            shared.append(f"Same location pattern: {first['location_pattern']}")
        words1 = set((first["mo_summary"] or "").lower().split())
        words2 = set((second["mo_summary"] or "").lower().split())
        mo_overlap = len(words1 & words2) / max(len(words1 | words2), 1) * 100
        return success_response(data={
            "pattern_1": first,
            "pattern_2": second,
            "shared_characteristics": shared,
            "mo_overlap": round(mo_overlap, 1),
            "overlap_score": round((len(shared) / 3 * 50) + (mo_overlap * 0.5), 1),
        })
    if not (p1_id.isdigit() and p2_id.isdigit()):
        return success_response(message="Pattern not found")
    svc = get_service(db)
    result = await svc.compare_patterns(int(p1_id), int(p2_id))
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result)


@router.get("/{pattern_id}")
async def get_pattern(pattern_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import pattern_occurrences

        ctx, patterns = await _phase1_patterns()
        match = next((p for p in patterns if str(p["id"]) == str(pattern_id)), None)
        if not match:
            return success_response(message="Pattern not found")
        return success_response(data={**match, "occurrences": pattern_occurrences(match, ctx)})
    if not pattern_id.isdigit():
        return success_response(message="Pattern not found")
    svc = get_service(db)
    pattern = await svc.get_pattern(int(pattern_id))
    if not pattern:
        return success_response(message="Pattern not found")
    return success_response(data=pattern)


@router.get("/{pattern_id}/occurrences")
async def get_pattern_occurrences(pattern_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import pattern_occurrences

        ctx, patterns = await _phase1_patterns()
        match = next((p for p in patterns if str(p["id"]) == str(pattern_id)), None)
        occurrences = pattern_occurrences(match, ctx) if match else []
        return success_response(data={"items": occurrences, "total": len(occurrences)})
    if not pattern_id.isdigit():
        return success_response(data={"items": [], "total": 0})
    svc = get_service(db)
    occurrences = await svc.get_pattern_occurrences(int(pattern_id))
    return success_response(data={"items": occurrences, "total": len(occurrences)})
