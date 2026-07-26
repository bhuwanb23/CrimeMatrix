from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from app.db.session import get_db
from app.services.early_warning_service import EarlyWarningService
from app.core.response import success_response
from app.db.phase1_store import using_phase1_store

router = APIRouter()


async def _phase1_alerts():
    from app.db.phase1_aggregations import derive_early_alerts, fetch_all_safe, resolve_names

    crimes = await fetch_all_safe("crimes")
    return derive_early_alerts(
        crimes,
        await resolve_names("districts"),
        await resolve_names("crime_types"),
    )


class AcknowledgeRequest(BaseModel):
    acknowledged_by: str = "Officer"


class RuleCreateRequest(BaseModel):
    name: str
    rule_type: str
    threshold: float = 0
    action: str = ""
    condition_json: Optional[str] = None


def get_service(db: AsyncSession):
    return EarlyWarningService(db)


@router.get("/stats")
async def early_warning_stats(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        alerts = await _phase1_alerts()
        return success_response(data={
            "total": len(alerts),
            "active": sum(1 for a in alerts if a.get("status") == "active"),
            "critical": sum(1 for a in alerts if a.get("severity") == "critical"),
            "high": sum(1 for a in alerts if a.get("severity") == "high"),
        })
    svc = get_service(db)
    return success_response(data=await svc.get_stats())


@router.get("/alerts")
async def list_alerts(
    status: str = Query(default=None),
    severity: str = Query(default=None),
    alert_type: str = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        alerts = await _phase1_alerts()
        if status:
            alerts = [a for a in alerts if a.get("status") == status]
        if severity:
            alerts = [a for a in alerts if a.get("severity") == severity]
        if alert_type:
            alerts = [a for a in alerts if a.get("alert_type") == alert_type]
        return success_response(data={"items": alerts, "total": len(alerts)})
    svc = get_service(db)
    alerts = await svc.get_alerts(status, severity, alert_type)
    return success_response(data={"items": alerts, "total": len(alerts)})


@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        alerts = await _phase1_alerts()
        match = next((a for a in alerts if str(a.get("id")) == str(alert_id)), None)
        if not match:
            return success_response(message="Alert not found")
        return success_response(data=match)
    if not alert_id.isdigit():
        return success_response(message="Alert not found")
    alert_id = int(alert_id)
    svc = get_service(db)
    alert = await svc.get_alert(alert_id)
    if not alert:
        return success_response(message="Alert not found")
    return success_response(data=alert)


@router.put("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: int, data: AcknowledgeRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.acknowledge_alert(alert_id, data.acknowledged_by)
    if "error" in result:
        return success_response(message=result["error"])
    return success_response(data=result, message="Alert acknowledged")


@router.get("/rules")
async def list_rules(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    rules = await svc.get_rules()
    return success_response(data={"items": rules, "total": len(rules)})


@router.post("/rules")
async def create_rule(data: RuleCreateRequest, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    result = await svc.create_rule(data.name, data.rule_type, data.threshold, data.action, data.condition_json)
    return success_response(data=result, message="Rule created")


@router.get("/timeline")
async def alert_timeline(
    days: int = Query(default=30),
    db: AsyncSession = Depends(get_db),
):
    if using_phase1_store():
        alerts = await _phase1_alerts()
        return success_response(data={"items": alerts, "total": len(alerts)})
    svc = get_service(db)
    timeline = await svc.get_timeline(days)
    return success_response(data={"items": timeline, "total": len(timeline)})


@router.post("/detect")
async def detect_alerts(db: AsyncSession = Depends(get_db)):
    if using_phase1_store():
        alerts = await _phase1_alerts()
        return success_response(
            data={"alerts_created": len(alerts), "alerts_found": len(alerts), "items": alerts},
            message="Detection complete",
        )
    svc = get_service(db)
    result = await svc.detect_alerts()
    return success_response(data=result, message="Detection complete")
