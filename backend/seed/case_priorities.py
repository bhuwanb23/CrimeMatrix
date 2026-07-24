from sqlalchemy import select

from seed.utils import get_one
from app.models.case_priority import CasePriority
from app.models.investigation import Investigation


async def seed(db) -> int:
    investigations = (await db.execute(select(Investigation))).scalars().all()
    n = 0
    for inv in investigations:
        if await get_one(db, CasePriority, investigation_id=inv.id):
            continue
        level = inv.priority or "medium"
        score = {"critical": 95, "high": 80, "medium": 55, "low": 30}.get(level, 50)
        db.add(CasePriority(
            investigation_id=inv.id,
            overall_priority_score=score,
            severity_score=score * 0.9,
            victim_vulnerability_score=score * 0.6,
            evidence_availability_score=score * 0.7,
            repeat_offender_score=score * 0.5,
            active_threats_score=score * 0.4,
            investigation_age_score=40,
            cross_district_score=20,
            officer_workload_score=50,
            priority_level=level,
            explanation_json=f'{{"summary":"Seeded priority for investigation {inv.id}"}}',
        ))
        n += 1
    await db.flush()
    return n
