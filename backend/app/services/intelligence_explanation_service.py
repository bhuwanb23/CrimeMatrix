import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.intelligence_event import IntelligenceEvent
from app.models.officer_intel import Recommendation
from app.models.evidence_link import EvidenceLink
from app.models.early_warning_alert import EarlyWarningAlert
from app.models.case import Case
from app.models.evidence import Evidence
from app.models.suspect import Suspect
from app.models.crime import Crime
from app.models.case_similarity import CaseSimilarity
from app.models.case_priority import CasePriority
from app.models.case_link import CaseLink
from app.models.investigation import Investigation
import structlog

logger = structlog.get_logger()


class IntelligenceExplanationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def explain_event(self, event_id: int) -> dict:
        stmt = select(IntelligenceEvent).where(IntelligenceEvent.id == event_id)
        result = await self.db.execute(stmt)
        event = result.scalar()
        if not event:
            return {"error": "Event not found"}

        event_type = event.event_type
        entity_id = event.entity_id
        entity_type = event.entity_type

        context = await self._gather_event_context(event_type, entity_id, entity_type)

        chain = self._build_reasoning_chain(event_type, context)
        confidence = self._calculate_confidence(chain)
        explanation = self._generate_explanation(event_type, context)
        evidence_list = self._gather_supporting_evidence(event_type, context)
        actions = self._suggest_actions(event_type, context)

        return {
            "event_id": event_id,
            "event_type": event_type,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "explanation": explanation,
            "reasoning_chain": chain,
            "confidence": confidence,
            "supporting_evidence": evidence_list,
            "recommended_actions": actions,
        }

    async def explain_recommendation(self, rec_id: int) -> dict:
        stmt = select(Recommendation).where(Recommendation.id == rec_id)
        result = await self.db.execute(stmt)
        rec = result.scalar()
        if not rec:
            return {"error": "Recommendation not found"}

        rec_type = rec.rec_type or ""
        entity_id = rec.entity_id
        context = await self._gather_recommendation_context(rec_type, rec)

        chain = self._build_rec_reasoning_chain(rec_type, context)
        confidence = self._calculate_confidence(chain)
        explanation = self._generate_rec_explanation(rec_type, context, rec)
        evidence_list = self._gather_rec_evidence(rec_type, context)
        actions = self._suggest_rec_actions(rec_type, context)

        return {
            "recommendation_id": rec_id,
            "rec_type": rec_type,
            "entity_type": rec.entity_type,
            "entity_id": entity_id,
            "explanation": explanation,
            "reasoning_chain": chain,
            "confidence": confidence,
            "supporting_evidence": evidence_list,
            "recommended_actions": actions,
        }

    async def explain_evidence_link(self, link_id: int) -> dict:
        stmt = select(EvidenceLink).where(EvidenceLink.id == link_id)
        result = await self.db.execute(stmt)
        link = result.scalar()
        if not link:
            return {"error": "Evidence link not found"}

        context = await self._gather_evidence_link_context(link)

        chain = [
            {"step": 1, "claim": f"Evidence #{link.evidence_id_1} linked to Evidence #{link.evidence_id_2}",
             "evidence_type": link.link_type or "correlation", "confidence": link.confidence or 70},
            {"step": 2, "claim": link.link_reason or "Pattern-based correlation detected",
             "evidence_type": "analysis", "confidence": link.confidence or 70},
        ]
        if context.get("ev1") and context.get("ev2"):
            ev1, ev2 = context["ev1"], context["ev2"]
            if ev1.get("crime_id") == ev2.get("crime_id"):
                chain.append({"step": 3, "claim": "Both evidence items belong to the same case",
                              "evidence_type": "case_link", "confidence": 90})

        confidence = self._calculate_confidence(chain)
        explanation = (
            f"Evidence items #{link.evidence_id_1} and #{link.evidence_id_2} were linked "
            f"because {link.link_reason or 'pattern analysis detected a correlation'}. "
            f"This link has {link.confidence or 70}% confidence based on "
            f"{link.link_type or 'shared characteristics'}."
        )

        return {
            "link_id": link_id,
            "link_type": link.link_type,
            "explanation": explanation,
            "reasoning_chain": chain,
            "confidence": confidence,
            "supporting_evidence": [
                {"type": link.link_type or "correlation", "description": link.link_reason or "Pattern match",
                 "strength": (link.confidence or 70) / 100.0},
            ],
            "recommended_actions": ["Review linked evidence items", "Check for additional connections",
                                     "Verify in case notes"],
        }

    async def explain_alert(self, alert_id: int) -> dict:
        stmt = select(EarlyWarningAlert).where(EarlyWarningAlert.id == alert_id)
        result = await self.db.execute(stmt)
        alert = result.scalar()
        if not alert:
            return {"error": "Alert not found"}

        chain = [
            {"step": 1, "claim": f"Alert triggered: {alert.alert_type or 'warning'}",
             "evidence_type": "alert_trigger", "confidence": 85},
            {"step": 2, "claim": f"Severity: {alert.severity or 'medium'}",
             "evidence_type": "severity_assessment", "confidence": 80},
        ]
        if alert.description:
            chain.append({"step": 3, "claim": alert.description,
                           "evidence_type": "detail", "confidence": 75})

        confidence = self._calculate_confidence(chain)
        explanation = (
            f"This alert was generated because the system detected "
            f"{alert.alert_type or 'an anomalous pattern'}. "
            f"{alert.description or 'The pattern met the threshold for automatic alerting.'} "
            f"Severity level: {alert.severity or 'medium'}."
        )

        return {
            "alert_id": alert_id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "explanation": explanation,
            "reasoning_chain": chain,
            "confidence": confidence,
            "supporting_evidence": [
                {"type": "alert", "description": alert.description or "Pattern detected",
                 "strength": 0.85},
            ],
            "recommended_actions": ["Investigate alert trigger", "Review related cases",
                                     "Check for patterns", "Update case status"],
        }

    async def _gather_event_context(self, event_type, entity_id, entity_type) -> dict:
        ctx = {"event_type": event_type, "entity_id": entity_id, "entity_type": entity_type}
        if not entity_id:
            return ctx

        try:
            if entity_type == "crime" or event_type == "crime_update":
                case = await self._load_model(Case, entity_id)
                if case:
                    ctx["case"] = {"id": case.id, "title": case.title, "crime_type": case.crime_type,
                                   "district": case.district, "status": case.status}
                    sims = await self._query_similar(case.id)
                    if sims:
                        ctx["similar_cases"] = sims
            elif entity_type == "evidence" or event_type == "evidence_update":
                ev = await self._load_model(Evidence, entity_id)
                if ev:
                    ctx["evidence"] = {"id": ev.id, "case_id": ev.case_id}
            elif entity_type == "investigation":
                inv = await self._load_model(Investigation, entity_id)
                if inv:
                    ctx["investigation"] = {"id": inv.id, "title": inv.title, "status": inv.status,
                                             "progress": inv.progress}
        except Exception as e:
            logger.warning("context_gather_error", error=str(e))

        return ctx

    async def _gather_recommendation_context(self, rec_type, rec) -> dict:
        ctx = {"rec_type": rec_type}
        try:
            if rec_type == "similar_case" and rec.entity_id:
                case = await self._load_model(Case, rec.entity_id)
                if case:
                    ctx["case"] = {"id": case.id, "title": case.title, "crime_type": case.crime_type,
                                   "district": case.district}
            elif rec_type == "suspect_alert" and rec.entity_id:
                suspect = await self._load_model(Suspect, rec.entity_id)
                if suspect:
                    ctx["suspect"] = {"id": suspect.id, "name": suspect.name, "district": suspect.district,
                                       "risk_score": suspect.risk_score}
            elif rec_type == "priority_escalation" and rec.entity_id:
                pri = await self._load_model(CasePriority, rec.entity_id, "case_id")
                if pri:
                    ctx["priority"] = {"overall_score": pri.overall_score}
            elif rec_type in ("evidence_review", "officer_assignment", "related_investigation"):
                if rec.entity_id:
                    case = await self._load_model(Case, rec.entity_id)
                    if case:
                        ctx["case"] = {"id": case.id, "title": case.title, "district": case.district}
        except Exception as e:
            logger.warning("rec_context_error", error=str(e))
        return ctx

    async def _gather_evidence_link_context(self, link) -> dict:
        ctx = {}
        try:
            ev1 = await self._load_model(Evidence, link.evidence_id_1)
            ev2 = await self._load_model(Evidence, link.evidence_id_2)
            if ev1:
                ctx["ev1"] = {"id": ev1.id, "case_id": ev1.case_id}
            if ev2:
                ctx["ev2"] = {"id": ev2.id, "case_id": ev2.case_id}
        except Exception:
            pass
        return ctx

    def _build_reasoning_chain(self, event_type, context) -> List[dict]:
        chain = []
        step = 1
        chain.append({"step": step, "claim": f"Event type: {event_type}",
                       "evidence_type": "event_classification", "confidence": 95})
        step += 1

        if context.get("case"):
            c = context["case"]
            chain.append({"step": step, "claim": f"Related to case: {c.get('title', 'Unknown')} ({c.get('crime_type', '?')} in {c.get('district', '?')})",
                           "evidence_type": "case_reference", "confidence": 90})
            step += 1

        if context.get("similar_cases"):
            n = len(context["similar_cases"])
            chain.append({"step": step, "claim": f"{n} similar case(s) found in database",
                           "evidence_type": "similarity_match", "confidence": 85})
            step += 1

        if context.get("evidence"):
            chain.append({"step": step, "claim": f"Evidence item #{context['evidence']['id']} linked to case #{context['evidence']['case_id']}",
                           "evidence_type": "evidence_link", "confidence": 88})
            step += 1

        if context.get("investigation"):
            inv = context["investigation"]
            chain.append({"step": step, "claim": f"Investigation '{inv.get('title', '')}' at {inv.get('progress', 0)}% progress",
                           "evidence_type": "investigation_status", "confidence": 80})

        return chain

    def _build_rec_reasoning_chain(self, rec_type, context) -> List[dict]:
        chain = []
        step = 1
        type_labels = {
            "similar_case": "Similar case analysis",
            "suspect_alert": "High-risk suspect detection",
            "cross_district": "Cross-district pattern analysis",
            "mo_pattern": "Modus operandi pattern matching",
            "evidence_review": "Evidence review recommendation",
            "officer_assignment": "Officer workload analysis",
            "priority_escalation": "Priority threshold exceeded",
            "related_investigation": "Related investigation detection",
        }
        chain.append({"step": step, "claim": type_labels.get(rec_type, f"Recommendation type: {rec_type}"),
                       "evidence_type": "analysis_type", "confidence": 90})
        step += 1

        if context.get("case"):
            c = context["case"]
            chain.append({"step": step, "claim": f"Case: {c.get('title', 'Unknown')} in {c.get('district', '?')}",
                           "evidence_type": "case_reference", "confidence": 88})
            step += 1

        if context.get("suspect"):
            s = context["suspect"]
            chain.append({"step": step, "claim": f"Suspect: {s.get('name', '?')} — risk score: {s.get('risk_score', 0):.0%}",
                           "evidence_type": "suspect_risk", "confidence": 85})
            step += 1

        if context.get("priority"):
            p = context["priority"]
            chain.append({"step": step, "claim": f"Priority score: {p.get('overall_score', 0):.0f}/100",
                           "evidence_type": "priority_assessment", "confidence": 82})

        return chain

    def _calculate_confidence(self, chain: List[dict]) -> dict:
        if not chain:
            return {"score": 50, "level": "low"}
        avg = sum(c.get("confidence", 50) for c in chain) / len(chain)
        score = round(avg, 1)
        if score >= 85:
            level = "high"
        elif score >= 65:
            level = "medium"
        else:
            level = "low"
        return {"score": score, "level": level}

    def _generate_explanation(self, event_type, context) -> str:
        type_names = {
            "crime_update": "A crime report was updated",
            "evidence_update": "New evidence was submitted",
            "case_update": "A case status changed",
            "investigation": "An investigation event occurred",
        }
        base = type_names.get(event_type, f"An intelligence event ({event_type}) was detected")
        parts = [base]

        if context.get("case"):
            c = context["case"]
            parts.append(f"involving case '{c.get('title', 'Unknown')}' ({c.get('crime_type', '?')} in {c.get('district', '?')})")

        if context.get("similar_cases"):
            n = len(context["similar_cases"])
            parts.append(f"The system found {n} similar case(s) that may be related")

        parts.append("This event was automatically processed by the AI Intelligence Engine to detect hidden relationships and recommend actions.")
        return " ".join(parts) + "."

    def _generate_rec_explanation(self, rec_type, context, rec) -> str:
        title = rec.title or rec.recommendation or ""
        desc = rec.description or ""
        reasons = self._parse_json_list(rec.reasons_json)

        parts = [f"This recommendation was generated because"]

        type_reasons = {
            "similar_case": "a case with similar characteristics was identified",
            "suspect_alert": "a suspect with elevated risk was detected",
            "cross_district": "patterns were found across multiple districts",
            "mo_pattern": "a matching modus operandi was identified",
            "evidence_review": "evidence items need to be reviewed",
            "officer_assignment": "a case needs officer assignment",
            "priority_escalation": "the priority score exceeded the threshold",
            "related_investigation": "related investigations were discovered",
        }
        parts.append(type_reasons.get(rec_type, f"analysis detected a match (type: {rec_type})"))

        if reasons:
            parts.append(f"Key factors: {'; '.join(reasons[:3])}")

        return " ".join(parts) + "."

    def _gather_supporting_evidence(self, event_type, context) -> List[dict]:
        evidence = []
        if context.get("case"):
            c = context["case"]
            evidence.append({"type": "case", "description": f"Case: {c.get('title', '')} ({c.get('crime_type', '')})",
                              "strength": 0.9})
        if context.get("similar_cases"):
            evidence.append({"type": "similarity", "description": f"{len(context['similar_cases'])} similar cases found",
                              "strength": 0.85})
        if context.get("evidence"):
            evidence.append({"type": "evidence", "description": f"Evidence #{context['evidence']['id']} in case #{context['evidence']['case_id']}",
                              "strength": 0.8})
        if context.get("investigation"):
            inv = context["investigation"]
            evidence.append({"type": "investigation", "description": f"Investigation: {inv.get('title', '')}",
                              "strength": 0.75})
        return evidence

    def _gather_rec_evidence(self, rec_type, context) -> List[dict]:
        evidence = []
        if context.get("case"):
            c = context["case"]
            evidence.append({"type": "case", "description": f"Case: {c.get('title', '')}", "strength": 0.85})
        if context.get("suspect"):
            s = context["suspect"]
            evidence.append({"type": "suspect", "description": f"Suspect: {s.get('name', '')} (risk: {s.get('risk_score', 0):.0%})",
                              "strength": 0.8})
        if context.get("priority"):
            p = context["priority"]
            evidence.append({"type": "priority", "description": f"Priority score: {p.get('overall_score', 0):.0f}",
                              "strength": 0.82})
        return evidence

    def _suggest_actions(self, event_type, context) -> List[str]:
        actions = []
        if event_type == "crime_update":
            actions.extend(["Review updated case details", "Check for new evidence", "Compare with similar cases"])
        elif event_type == "evidence_update":
            actions.extend(["Review new evidence", "Check for evidence links", "Update investigation notes"])
        elif event_type == "case_update":
            actions.extend(["Review case progress", "Check recommendations", "Update team status"])
        else:
            actions.extend(["Investigate further", "Review related data", "Update case notes"])
        return actions

    def _suggest_rec_actions(self, rec_type, context) -> List[str]:
        actions = {
            "similar_case": ["Review similar case", "Compare evidence", "Check MO patterns"],
            "suspect_alert": ["Investigate suspect", "Review criminal history", "Check locations"],
            "cross_district": ["Coordinate with other districts", "Share intelligence", "Joint investigation"],
            "mo_pattern": ["Analyze MO fingerprint", "Search for related crimes", "Update pattern database"],
            "evidence_review": ["Review evidence items", "Check for links", "Update chain of custody"],
            "officer_assignment": ["Assign officer", "Check workload", "Update case assignment"],
            "priority_escalation": ["Escalate to supervisor", "Allocate more resources", "Review priority factors"],
            "related_investigation": ["Coordinate investigations", "Share findings", "Link case files"],
        }
        return actions.get(rec_type, ["Review recommendation", "Take appropriate action"])

    def _parse_json_list(self, json_str: str) -> List[str]:
        if not json_str:
            return []
        try:
            return json.loads(json_str)
        except Exception:
            return []

    async def _load_model(self, model_class, entity_id: int, id_column: str = "id"):
        stmt = select(model_class).where(getattr(model_class, id_column) == entity_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _query_similar(self, case_id: int, limit: int = 3) -> List[dict]:
        stmt = (
            select(CaseSimilarity)
            .where(CaseSimilarity.case_id_1 == case_id, CaseSimilarity.status == "active")
            .order_by(CaseSimilarity.overall_score.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        sims = result.scalars().all()
        return [{"id": s.id, "case_id_2": s.case_id_2, "score": s.overall_score} for s in sims]
