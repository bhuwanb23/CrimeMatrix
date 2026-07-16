from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from app.db.session import get_db
from app.models.case import Case
from app.models.suspect import Suspect
from app.models.user import User
from app.models.alert import Alert
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
    })
