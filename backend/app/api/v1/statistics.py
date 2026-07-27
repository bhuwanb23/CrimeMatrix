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
from app.db.phase1_store import store_list, using_phase1_store

router = APIRouter()


@router.get("/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        from app.db.phase1_aggregations import fetch_all

        cases = await fetch_all("cases")
        crimes = await fetch_all("crimes")
        suspects = await fetch_all("suspects")
        officers = await store_list("officers", page=1, page_size=1)
        crime_types = await store_list("crime_types", page=1, page_size=1)
        case_statuses = await store_list("case_status_master", page=1, page_size=1)
        crime_heads = await store_list("crime_heads", page=1, page_size=1)
        crime_sub_heads = await store_list("crime_sub_heads", page=1, page_size=1)
        categories = await store_list("case_categories", page=1, page_size=1)

        total_cases = len(cases)
        total_crimes = len(crimes)
        # Prefer cases once seeded 1:1; fall back to crimes if cases table is still sparse
        display_total = total_cases if total_cases >= total_crimes else total_crimes
        status_rows = cases if total_cases >= total_crimes else crimes
        active_cases = sum(1 for c in status_rows if str(c.get("status") or "").lower() in {"active", "open"})
        closed_cases = sum(1 for c in status_rows if str(c.get("status") or "").lower() in {"closed", "resolved"})
        pending = max(0, display_total - active_cases - closed_cases)

        return success_response(
            data={
                "totals": {
                    "users": officers.get("total", 0),
                    "cases": display_total,
                    "crimes": total_crimes,
                    "suspects": len(suspects),
                    "alerts": sum(1 for s in suspects if float(s.get("risk_score") or 0) >= 0.5),
                },
                "cases_by_status": {
                    "active": active_cases,
                    "closed": closed_cases,
                    "pending": pending,
                },
                "resolution_rate": round((closed_cases / display_total * 100), 1) if display_total else 0,
                "lookups": {
                    "categories": categories.get("total", 0),
                    "gravity_offences": 0,
                    "crime_heads": crime_heads.get("total", 0),
                    "crime_sub_heads": crime_sub_heads.get("total", 0),
                    "case_statuses": case_statuses.get("total", 0),
                    "courts": 0,
                    "crime_types": crime_types.get("total", 0),
                },
                "source": "phase1_store",
            }
        )

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
