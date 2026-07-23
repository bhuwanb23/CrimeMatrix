from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.db.session import get_db
from app.models.case import Case
from app.models.suspect import Suspect
from app.models.user import User
from app.models.alert import Alert
from app.models.case_category import CaseCategory
from app.models.gravity_offence import GravityOffence
from app.models.crime_head import CrimeHead
from app.models.crime_sub_head import CrimeSubHead
from app.models.case_status_master import CaseStatusMaster
from app.models.court import Court
from app.core.response import success_response

router = APIRouter()


@router.get("/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select

    # Total counts
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar() or 0

    cases_result = await db.execute(select(func.count(Case.id)))
    total_cases = cases_result.scalar() or 0

    suspects_result = await db.execute(select(func.count(Suspect.id)))
    total_suspects = suspects_result.scalar() or 0

    alerts_result = await db.execute(select(func.count(Alert.id)))
    total_alerts = alerts_result.scalar() or 0

    # Cases by status
    active_result = await db.execute(
        select(func.count(Case.id)).where(Case.status == 'active')
    )
    active_cases = active_result.scalar() or 0

    closed_result = await db.execute(
        select(func.count(Case.id)).where(Case.status == 'closed')
    )
    closed_cases = closed_result.scalar() or 0

    # Lookup table counts
    categories_result = await db.execute(select(func.count(CaseCategory.id)))
    gravity_result = await db.execute(select(func.count(GravityOffence.id)))
    heads_result = await db.execute(select(func.count(CrimeHead.id)))
    sub_heads_result = await db.execute(select(func.count(CrimeSubHead.id)))
    statuses_result = await db.execute(select(func.count(CaseStatusMaster.id)))
    courts_result = await db.execute(select(func.count(Court.id)))

    return success_response(data={
        "totals": {
            "users": total_users,
            "cases": total_cases,
            "suspects": total_suspects,
            "alerts": total_alerts,
        },
        "cases_by_status": {
            "active": active_cases,
            "closed": closed_cases,
            "pending": total_cases - active_cases - closed_cases,
        },
        "resolution_rate": round((closed_cases / total_cases * 100), 1) if total_cases > 0 else 0,
        "lookups": {
            "categories": categories_result.scalar() or 0,
            "gravity_offences": gravity_result.scalar() or 0,
            "crime_heads": heads_result.scalar() or 0,
            "crime_sub_heads": sub_heads_result.scalar() or 0,
            "case_statuses": statuses_result.scalar() or 0,
            "courts": courts_result.scalar() or 0,
        },
    })
