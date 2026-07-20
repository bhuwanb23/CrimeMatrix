import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.district import District
from app.models.early_warning_alert import EarlyWarningAlert
from app.models.alert_rule import AlertRule
from app.models.alert_event import AlertEvent
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class EarlyWarningService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def detect_alerts(self) -> dict:
        alerts_created = 0

        # 1. Detect crime spikes
        spike_alerts = await self._detect_spikes()
        alerts_created += len(spike_alerts)

        # 2. Detect emerging hotspots
        hotspot_alerts = await self._detect_hotspot_escalation()
        alerts_created += len(hotspot_alerts)

        # 3. Detect serial offense patterns
        serial_alerts = await self._detect_serial_offenses()
        alerts_created += len(serial_alerts)

        # 4. Detect cross-district escalation
        escalation_alerts = await self._detect_escalation()
        alerts_created += len(escalation_alerts)

        return {
            "alerts_created": alerts_created,
            "spike_alerts": len(spike_alerts),
            "hotspot_alerts": len(hotspot_alerts),
            "serial_alerts": len(serial_alerts),
            "escalation_alerts": len(escalation_alerts),
        }

    async def get_alerts(self, status: str = None, severity: str = None,
                         alert_type: str = None) -> List[dict]:
        stmt = select(EarlyWarningAlert)
        if status:
            stmt = stmt.where(EarlyWarningAlert.status == status)
        if severity:
            stmt = stmt.where(EarlyWarningAlert.severity == severity)
        if alert_type:
            stmt = stmt.where(EarlyWarningAlert.alert_type == alert_type)
        stmt = stmt.order_by(EarlyWarningAlert.created_at.desc())
        result = await self.db.execute(stmt)
        return [self._alert_to_dict(a) for a in result.scalars().all()]

    async def get_alert(self, alert_id: int) -> Optional[dict]:
        stmt = select(EarlyWarningAlert).where(EarlyWarningAlert.id == alert_id)
        result = await self.db.execute(stmt)
        a = result.scalar()
        if not a:
            return None
        events = await self._get_events(alert_id)
        return {**self._alert_to_dict(a), "events": events}

    async def acknowledge_alert(self, alert_id: int, acknowledged_by: str = "Officer") -> dict:
        stmt = select(EarlyWarningAlert).where(EarlyWarningAlert.id == alert_id)
        result = await self.db.execute(stmt)
        alert = result.scalar()
        if not alert:
            return {"error": "Alert not found"}

        alert.status = "acknowledged"
        alert.acknowledged_by = acknowledged_by
        alert.acknowledged_at = datetime.utcnow()

        event = AlertEvent(
            alert_id=alert_id,
            event_type="acknowledged",
            message=f"Alert acknowledged by {acknowledged_by}",
            created_by=acknowledged_by,
        )
        self.db.add(event)
        await self.db.commit()
        return {"id": alert_id, "status": "acknowledged"}

    async def get_rules(self) -> List[dict]:
        stmt = select(AlertRule).order_by(AlertRule.created_at.desc())
        result = await self.db.execute(stmt)
        return [self._rule_to_dict(r) for r in result.scalars().all()]

    async def create_rule(self, name: str, rule_type: str, threshold: float = 0,
                          action: str = "", condition_json: str = None) -> dict:
        rule = AlertRule(
            name=name,
            rule_type=rule_type,
            threshold=threshold,
            action=action,
            condition_json=condition_json,
        )
        self.db.add(rule)
        await self.db.commit()
        await self.db.refresh(rule)
        return {"id": rule.id, "name": rule.name, "rule_type": rule.rule_type}

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(EarlyWarningAlert.id)))).scalar() or 0
        active = (await self.db.execute(
            select(sql_func.count(EarlyWarningAlert.id)).where(EarlyWarningAlert.status == "active")
        )).scalar() or 0
        critical = (await self.db.execute(
            select(sql_func.count(EarlyWarningAlert.id)).where(EarlyWarningAlert.severity == "critical")
        )).scalar() or 0
        high = (await self.db.execute(
            select(sql_func.count(EarlyWarningAlert.id)).where(EarlyWarningAlert.severity == "high")
        )).scalar() or 0
        return {"total": total, "active": active, "critical": critical, "high": high}

    async def get_timeline(self, days: int = 30) -> List[dict]:
        date_from = datetime.utcnow() - timedelta(days=days)
        stmt = select(EarlyWarningAlert).where(
            EarlyWarningAlert.created_at >= date_from
        ).order_by(EarlyWarningAlert.created_at.desc())
        result = await self.db.execute(stmt)
        return [self._alert_to_dict(a) for a in result.scalars().all()]

    async def _detect_spikes(self) -> List[dict]:
        alerts = []
        date_from = datetime.utcnow() - timedelta(days=7)
        date_prev = datetime.utcnow() - timedelta(days=14)

        stmt = select(
            Crime.district_id,
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by(Crime.district_id)
        result = await self.db.execute(stmt)
        recent = {r[0]: r[1] for r in result.all()}

        stmt2 = select(
            Crime.district_id,
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_prev, Crime.created_at < date_from).group_by(Crime.district_id)
        result2 = await self.db.execute(stmt2)
        previous = {r[0]: r[1] for r in result2.all()}

        for district_id, recent_count in recent.items():
            prev_count = previous.get(district_id, 0)
            if prev_count > 0 and recent_count > prev_count * 1.5:
                increase = ((recent_count - prev_count) / prev_count) * 100
                district_name = await self._get_district_name(district_id)
                alert = EarlyWarningAlert(
                    alert_type="spike",
                    title=f"Crime Spike in {district_name}",
                    description=f"Crime rate increased by {increase:.0f}% compared to previous week",
                    severity="high" if increase > 100 else "medium",
                    district_id=district_id,
                    detected_value=recent_count,
                    threshold=prev_count * 1.5,
                    confidence=min(100, increase),
                    evidence_json=json.dumps({"recent": recent_count, "previous": prev_count, "increase": increase}),
                )
                self.db.add(alert)
                alerts.append(alert)

        await self.db.commit()
        return alerts

    async def _detect_hotspot_escalation(self) -> List[dict]:
        alerts = []
        date_from = datetime.utcnow() - timedelta(days=30)

        stmt = select(
            Crime.district_id,
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from).group_by(Crime.district_id)
        result = await self.db.execute(stmt)

        for district_id, count in result.all():
            if count > 15:
                district_name = await self._get_district_name(district_id)
                alert = EarlyWarningAlert(
                    alert_type="hotspot",
                    title=f"Emerging Hotspot: {district_name}",
                    description=f"{count} crimes in 30 days — potential hotspot",
                    severity="high" if count > 25 else "medium",
                    district_id=district_id,
                    detected_value=count,
                    threshold=15,
                    confidence=min(100, count * 4),
                    evidence_json=json.dumps({"crime_count": count, "period": "30d"}),
                )
                self.db.add(alert)
                alerts.append(alert)

        await self.db.commit()
        return alerts

    async def _detect_serial_offenses(self) -> List[dict]:
        alerts = []
        stmt = select(Crime).where(Crime.created_at >= datetime.utcnow() - timedelta(days=30))
        result = await self.db.execute(stmt)
        crimes = result.scalars().all()

        district_crimes = defaultdict(list)
        for c in crimes:
            if c.district_id:
                district_crimes[c.district_id].append(c)

        for district_id, dcrimes in district_crimes.items():
            if len(dcrimes) >= 5:
                district_name = await self._get_district_name(district_id)
                alert = EarlyWarningAlert(
                    alert_type="serial",
                    title=f"Serial Offenses in {district_name}",
                    description=f"{len(dcrimes)} similar crimes in 30 days — possible serial pattern",
                    severity="high" if len(dcrimes) > 8 else "medium",
                    district_id=district_id,
                    detected_value=len(dcrimes),
                    threshold=5,
                    confidence=min(100, len(dcrimes) * 12),
                    evidence_json=json.dumps({"crime_count": len(dcrimes), "period": "30d"}),
                )
                self.db.add(alert)
                alerts.append(alert)

        await self.db.commit()
        return alerts

    async def _detect_escalation(self) -> List[dict]:
        alerts = []
        date_from = datetime.utcnow() - timedelta(days=90)
        date_mid = datetime.utcnow() - timedelta(days=45)

        stmt = select(
            Crime.district_id,
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_mid).group_by(Crime.district_id)
        result = await self.db.execute(stmt)
        recent = {r[0]: r[1] for r in result.all()}

        stmt2 = select(
            Crime.district_id,
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from, Crime.created_at < date_mid).group_by(Crime.district_id)
        result2 = await self.db.execute(stmt2)
        previous = {r[0]: r[1] for r in result2.all()}

        for district_id, recent_count in recent.items():
            prev_count = previous.get(district_id, 0)
            if prev_count > 0 and recent_count > prev_count * 2:
                district_name = await self._get_district_name(district_id)
                alert = EarlyWarningAlert(
                    alert_type="escalation",
                    title=f"Crime Escalation: {district_name}",
                    description=f"Crime rate doubled compared to previous 45 days",
                    severity="critical",
                    district_id=district_id,
                    detected_value=recent_count,
                    threshold=prev_count * 2,
                    confidence=min(100, ((recent_count - prev_count) / max(prev_count, 1)) * 50),
                    evidence_json=json.dumps({"recent": recent_count, "previous": prev_count}),
                )
                self.db.add(alert)
                alerts.append(alert)

        await self.db.commit()
        return alerts

    async def _get_district_name(self, district_id: int) -> str:
        if not district_id:
            return "Unknown District"
        stmt = select(District.name).where(District.id == district_id)
        result = await self.db.execute(stmt)
        return result.scalar() or f"District #{district_id}"

    async def _get_events(self, alert_id: int) -> List[dict]:
        stmt = select(AlertEvent).where(AlertEvent.alert_id == alert_id).order_by(AlertEvent.created_at.desc())
        result = await self.db.execute(stmt)
        return [
            {"id": e.id, "event_type": e.event_type, "message": e.message, "created_by": e.created_by,
             "created_at": str(e.created_at) if e.created_at else None}
            for e in result.scalars().all()
        ]

    def _alert_to_dict(self, a: EarlyWarningAlert) -> dict:
        return {
            "id": a.id, "alert_type": a.alert_type, "title": a.title,
            "description": a.description, "severity": a.severity,
            "district_id": a.district_id, "confidence": a.confidence,
            "status": a.status, "acknowledged_by": a.acknowledged_by,
            "created_at": str(a.created_at) if a.created_at else None,
        }

    def _rule_to_dict(self, r: AlertRule) -> dict:
        return {
            "id": r.id, "name": r.name, "rule_type": r.rule_type,
            "threshold": r.threshold, "action": r.action, "is_active": r.is_active,
        }
