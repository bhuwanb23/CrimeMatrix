from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.investigation import Investigation
from app.services.investigation_service import InvestigationService
from app.services.similar_case_service import SimilarCaseService
import structlog

logger = structlog.get_logger()


class InvestigationAnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.inv_service = InvestigationService(db)
        self.similar_service = SimilarCaseService(db)

    async def analyze(self, investigation_id: int, analysis_type: str = "summary",
                      question: str = None) -> dict:
        investigation = await self.inv_service.get_investigation(investigation_id)
        if not investigation:
            return {"error": "Investigation not found", "context": "", "data": {}}

        similar_cases = []
        if investigation.get("case_id"):
            try:
                similar_cases = await self.similar_service.get_similar(investigation["case_id"], top_k=5)
            except Exception:
                similar_cases = []

        investigation["similar_cases"] = similar_cases

        if analysis_type == "summary":
            context = self._build_summary(investigation)
        elif analysis_type == "leads":
            context = self._build_leads(investigation)
        elif analysis_type == "evidence":
            context = self._build_evidence_review(investigation)
        elif analysis_type == "similar":
            context = self._build_similar_analysis(investigation)
        elif analysis_type == "full":
            context = self._build_full_report(investigation)
        else:
            context = self._build_summary(investigation)

        if question:
            context += f"\n\n## Officer's Question\n{question}"

        return {
            "context": context,
            "data": {
                "investigation_id": investigation_id,
                "title": investigation.get("title"),
                "status": investigation.get("status"),
                "progress": investigation.get("progress"),
                "notes_count": len(investigation.get("notes", [])),
                "evidence_count": len(investigation.get("evidence", [])),
                "timeline_count": len(investigation.get("timeline", [])),
                "similar_count": len(similar_cases),
                "analysis_type": analysis_type,
            },
        }

    def _build_summary(self, inv: dict) -> str:
        lines = [
            f"## Investigation Summary: {inv.get('title', 'Unknown')}",
            f"- Status: {inv.get('status', 'unknown')}",
            f"- Priority: {inv.get('priority', 'medium')}",
            f"- Progress: {inv.get('progress', 0)}%",
            f"- District: {inv.get('district', 'N/A')}",
            "",
        ]

        notes = inv.get("notes", [])
        if notes:
            lines.append("### Key Notes")
            for n in notes[:5]:
                lines.append(f"- {n.get('content', '')[:200]}")
            lines.append("")

        evidence = inv.get("evidence", [])
        if evidence:
            lines.append("### Evidence Collected")
            for e in evidence[:5]:
                lines.append(f"- [{e.get('evidence_type', 'Unknown')}] {e.get('description', '')[:150]} (Status: {e.get('status', 'pending')})")
            lines.append("")

        timeline = inv.get("timeline", [])
        if timeline:
            lines.append("### Timeline")
            for t in timeline[:5]:
                lines.append(f"- {t.get('title', '')} ({t.get('event_type', '')})")
            lines.append("")

        similar = inv.get("similar_cases", [])
        if similar:
            lines.append("### Similar Cases Found")
            for s in similar[:3]:
                lines.append(f"- Case #{s.get('case_id')}: {s.get('title', '')} (Score: {s.get('overall_score', 0)}%)")
            lines.append("")

        lines.append("Generate a concise investigation summary based on this data.")
        return "\n".join(lines)

    def _build_leads(self, inv: dict) -> str:
        lines = [
            f"## Lead Analysis: {inv.get('title', 'Unknown')}",
            f"- Status: {inv.get('status')}",
            f"- Progress: {inv.get('progress', 0)}%",
            "",
        ]

        notes = inv.get("notes", [])
        if notes:
            lines.append("### Current Notes")
            for n in notes:
                lines.append(f"- {n.get('content', '')[:200]}")
            lines.append("")

        evidence = inv.get("evidence", [])
        pending_evidence = [e for e in evidence if e.get("status") in ("pending", "Pending", "Under review")]
        if pending_evidence:
            lines.append("### Pending Evidence (Potential Leads)")
            for e in pending_evidence:
                lines.append(f"- [{e.get('evidence_type')}] {e.get('description', '')[:150]}")
            lines.append("")

        similar = inv.get("similar_cases", [])
        if similar:
            lines.append("### Similar Cases (Cross-reference Opportunities)")
            for s in similar[:3]:
                lines.append(f"- Case #{s.get('case_id')}: {s.get('title', '')} — Score: {s.get('overall_score', 0)}%")
                reasons = s.get("reasons", [])
                if reasons:
                    lines.append(f"  Reasons: {', '.join(reasons[:3])}")
            lines.append("")

        lines.append("Suggest 3-5 actionable leads based on this investigation data.")
        return "\n".join(lines)

    def _build_evidence_review(self, inv: dict) -> str:
        lines = [
            f"## Evidence Review: {inv.get('title', 'Unknown')}",
            "",
        ]

        evidence = inv.get("evidence", [])
        if not evidence:
            lines.append("No evidence has been collected yet.")
        else:
            lines.append(f"### Total Evidence Items: {len(evidence)}")
            lines.append("")

            analyzed = [e for e in evidence if e.get("status") in ("Analyzed", "analyzed")]
            pending = [e for e in evidence if e.get("status") in ("pending", "Pending")]
            review = [e for e in evidence if e.get("status") in ("Under review", "under_review")]

            if analyzed:
                lines.append("#### Analyzed")
                for e in analyzed:
                    lines.append(f"- [{e.get('evidence_type')}] {e.get('description', '')[:200]}")
                lines.append("")

            if review:
                lines.append("#### Under Review")
                for e in review:
                    lines.append(f"- [{e.get('evidence_type')}] {e.get('description', '')[:200]}")
                lines.append("")

            if pending:
                lines.append("#### Pending Analysis")
                for e in pending:
                    lines.append(f"- [{e.get('evidence_type')}] {e.get('description', '')[:200]}")
                lines.append("")

        lines.append("Provide a comprehensive evidence review with analysis of strengths and gaps.")
        return "\n".join(lines)

    def _build_similar_analysis(self, inv: dict) -> str:
        lines = [
            f"## Similar Case Analysis: {inv.get('title', 'Unknown')}",
            "",
        ]

        similar = inv.get("similar_cases", [])
        if not similar:
            lines.append("No similar cases found.")
        else:
            lines.append(f"### {len(similar)} Similar Cases Identified")
            lines.append("")
            for i, s in enumerate(similar, 1):
                lines.append(f"#### {i}. Case #{s.get('case_id')}: {s.get('title', '')}")
                lines.append(f"- Overall Score: {s.get('overall_score', 0)}%")
                lines.append(f"- MO Score: {s.get('mo_score', 0)}%")
                lines.append(f"- Location Score: {s.get('location_score', 0)}%")
                lines.append(f"- Time Score: {s.get('time_score', 0)}%")
                lines.append(f"- Suspects Score: {s.get('suspects_score', 0)}%")
                lines.append(f"- Evidence Score: {s.get('evidence_score', 0)}%")
                reasons = s.get("reasons", [])
                if reasons:
                    lines.append(f"- Reasons: {', '.join(reasons)}")
                lines.append("")

        lines.append("Analyze the similar cases and suggest cross-investigation strategies.")
        return "\n".join(lines)

    def _build_full_report(self, inv: dict) -> str:
        lines = [
            f"## Full Investigation Report: {inv.get('title', 'Unknown')}",
            f"Status: {inv.get('status')} | Priority: {inv.get('priority')} | Progress: {inv.get('progress', 0)}%",
            f"District: {inv.get('district', 'N/A')}",
            "",
        ]

        if inv.get("description"):
            lines.append(f"### Description\n{inv['description']}\n")

        notes = inv.get("notes", [])
        if notes:
            lines.append(f"### Notes ({len(notes)} total)")
            for n in notes:
                lines.append(f"- {n.get('content', '')[:200]}")
            lines.append("")

        evidence = inv.get("evidence", [])
        if evidence:
            lines.append(f"### Evidence ({len(evidence)} items)")
            for e in evidence:
                lines.append(f"- [{e.get('evidence_type')}] {e.get('description', '')[:150]} ({e.get('status')})")
            lines.append("")

        timeline = inv.get("timeline", [])
        if timeline:
            lines.append(f"### Timeline ({len(timeline)} events)")
            for t in timeline:
                lines.append(f"- {t.get('title', '')} — {t.get('event_type', '')}")
            lines.append("")

        similar = inv.get("similar_cases", [])
        if similar:
            lines.append(f"### Similar Cases ({len(similar)} found)")
            for s in similar[:5]:
                lines.append(f"- Case #{s.get('case_id')}: {s.get('title', '')} (Score: {s.get('overall_score', 0)}%)")
            lines.append("")

        status_logs = inv.get("status_logs", [])
        if status_logs:
            lines.append(f"### Status History ({len(status_logs)} changes)")
            for log in status_logs:
                lines.append(f"- {log.get('old_status', '?')} → {log.get('new_status', '?')}")
            lines.append("")

        lines.append("Generate a comprehensive investigation report with key findings, evidence assessment, and next steps.")
        return "\n".join(lines)
