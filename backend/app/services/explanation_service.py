import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime_prediction import CrimePrediction
from app.models.prediction_explanation_record import PredictionExplanationRecord
from app.models.prediction_source import PredictionSource
from app.models.crime import Crime
from app.models.district import District
import structlog
from datetime import datetime

logger = structlog.get_logger()


class ExplanationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def explain_prediction(self, prediction_id: int) -> dict:
        pred = await self._load_prediction(prediction_id)
        if not pred:
            return {"error": "Prediction not found"}

        factors = self._generate_factors(pred)
        confidence_breakdown = self._generate_confidence_breakdown(pred)
        evidence = self._generate_evidence(pred, prediction_id)
        model_explanation = self._generate_model_explanation(pred)

        # Save explanation
        existing = await self._explanation_exists(prediction_id)
        if existing:
            existing.contributing_factors = json.dumps(factors)
            existing.confidence_breakdown = json.dumps(confidence_breakdown)
            existing.model_explanation = model_explanation
            existing.evidence_links = json.dumps(evidence)
        else:
            explanation = PredictionExplanationRecord(
                prediction_id=prediction_id,
                explanation_type=pred.get("prediction_type", "forecast"),
                contributing_factors=json.dumps(factors),
                confidence_breakdown=json.dumps(confidence_breakdown),
                model_explanation=model_explanation,
                evidence_links=json.dumps(evidence),
            )
            self.db.add(explanation)

        # Save sources
        sources = await self._generate_sources(prediction_id, pred)
        for src in sources:
            existing_src = await self._source_exists(prediction_id, src["source_type"], src["source_id"])
            if not existing_src:
                ps = PredictionSource(
                    prediction_id=prediction_id,
                    source_type=src["source_type"],
                    source_id=src["source_id"],
                    source_name=src["source_name"],
                    relevance_score=src["relevance_score"],
                )
                self.db.add(ps)

        await self.db.commit()

        return {
            "prediction_id": prediction_id,
            "factors": factors,
            "confidence_breakdown": confidence_breakdown,
            "model_explanation": model_explanation,
            "evidence": evidence,
            "sources": sources,
        }

    async def get_explanation(self, prediction_id: int) -> Optional[dict]:
        stmt = select(PredictionExplanationRecord).where(
            PredictionExplanationRecord.prediction_id == prediction_id
        )
        result = await self.db.execute(stmt)
        exp = result.scalar()
        if not exp:
            return None
        sources = await self._get_sources(prediction_id)
        return {
            "prediction_id": prediction_id,
            "factors": json.loads(exp.contributing_factors) if exp.contributing_factors else [],
            "confidence_breakdown": json.loads(exp.confidence_breakdown) if exp.confidence_breakdown else {},
            "model_explanation": exp.model_explanation,
            "evidence": json.loads(exp.evidence_links) if exp.evidence_links else [],
            "sources": sources,
        }

    async def get_sources(self, prediction_id: int) -> List[dict]:
        return await self._get_sources(prediction_id)

    async def get_confidence_breakdown(self, prediction_id: int) -> dict:
        exp = await self._load_explanation(prediction_id)
        if not exp:
            return {"error": "No explanation found"}
        return {
            "prediction_id": prediction_id,
            "breakdown": json.loads(exp.get("confidence_breakdown", "{}")),
            "model_explanation": exp.get("model_explanation", ""),
        }

    def _generate_factors(self, pred: dict) -> List[dict]:
        factors = []
        pred_type = pred.get("prediction_type", "forecast")
        confidence = pred.get("confidence", 0)

        if pred_type == "forecast":
            factors.append({"name": "Historical Trend", "weight": 0.35, "description": "Based on crime rate trends over the past period"})
            factors.append({"name": "Seasonal Pattern", "weight": 0.25, "description": "Time-of-year and day-of-week patterns"})
            factors.append({"name": "District Activity", "weight": 0.20, "description": "Crime density in the target district"})
            factors.append({"name": "Model Confidence", "weight": 0.20, "description": f"Model confidence: {confidence}%"})
        elif pred_type == "risk":
            factors.append({"name": "Criminal History", "weight": 0.30, "description": "Prior offense records"})
            factors.append({"name": "Location Risk", "weight": 0.25, "description": "High-risk area indicators"})
            factors.append({"name": "Recency", "weight": 0.25, "description": "Time since last offense"})
            factors.append({"name": "Network Links", "weight": 0.20, "description": "Known associates with records"})
        else:
            factors.append({"name": "Data Patterns", "weight": 0.40, "description": "Historical data pattern analysis"})
            factors.append({"name": "Statistical Significance", "weight": 0.30, "description": "Statistical confidence in the prediction"})
            factors.append({"name": "External Factors", "weight": 0.30, "description": "Environmental and contextual factors"})

        return factors

    def _generate_confidence_breakdown(self, pred: dict) -> dict:
        confidence = pred.get("confidence", 0)
        return {
            "overall": confidence,
            "data_quality": min(100, confidence + 10),
            "model_reliability": min(100, confidence + 5),
            "temporal_stability": max(0, confidence - 10),
            "explanation": f"Confidence of {confidence}% based on data quality, model reliability, and temporal stability",
        }

    def _generate_evidence(self, pred: dict, prediction_id: int) -> List[dict]:
        evidence = []
        district_id = pred.get("district_id")
        if district_id:
            evidence.append({"type": "district", "id": district_id, "description": "District-level crime data"})
        crime_type_id = pred.get("crime_type_id")
        if crime_type_id:
            evidence.append({"type": "crime_type", "id": crime_type_id, "description": "Crime type historical data"})
        evidence.append({"type": "model", "id": pred.get("model_name", "unknown"), "description": f"Prediction model: {pred.get('model_name', 'unknown')}"})
        return evidence

    def _generate_model_explanation(self, pred: dict) -> str:
        pred_type = pred.get("prediction_type", "forecast")
        predicted = pred.get("predicted_value", 0)
        confidence = pred.get("confidence", 0)

        if pred_type == "forecast":
            return (
                f"This forecast predicts {predicted} incidents based on moving average analysis "
                f"of historical crime data. The model achieves {confidence}% confidence by "
                f"analyzing trend direction, seasonal patterns, and district-level activity. "
                f"Predictions are more reliable when historical data is consistent and abundant."
            )
        elif pred_type == "risk":
            return (
                f"This risk assessment scores the subject at {predicted}% based on "
                f"criminal history, location risk, recency of offenses, and network analysis. "
                f"Higher scores indicate greater risk of reoffending."
            )
        else:
            return (
                f"Prediction value: {predicted} with {confidence}% confidence. "
                f"Based on statistical analysis of historical patterns and current data trends."
            )

    async def _generate_sources(self, prediction_id: int, pred: dict) -> List[dict]:
        sources = []
        district_id = pred.get("district_id")
        if district_id:
            sources.append({"source_type": "district", "source_id": district_id, "source_name": f"District #{district_id}", "relevance_score": 0.8})
        sources.append({"source_type": "model", "source_id": 0, "source_name": pred.get("model_name", "moving_average"), "relevance_score": 1.0})
        sources.append({"source_type": "historical_data", "source_id": 0, "source_name": "Historical crime records", "relevance_score": 0.9})
        return sources

    async def _load_prediction(self, prediction_id: int) -> Optional[dict]:
        stmt = select(CrimePrediction).where(CrimePrediction.id == prediction_id)
        result = await self.db.execute(stmt)
        p = result.scalar()
        return {
            "id": p.id, "prediction_type": p.prediction_type,
            "district_id": p.district_id, "crime_type_id": p.crime_type_id,
            "predicted_value": p.predicted_value, "confidence": p.confidence,
            "model_name": p.model_name, "target_date": p.target_date,
        } if p else None

    async def _load_explanation(self, prediction_id: int) -> Optional[dict]:
        stmt = select(PredictionExplanationRecord).where(
            PredictionExplanationRecord.prediction_id == prediction_id
        )
        result = await self.db.execute(stmt)
        exp = result.scalar()
        return {
            "contributing_factors": exp.contributing_factors,
            "confidence_breakdown": exp.confidence_breakdown,
            "model_explanation": exp.model_explanation,
            "evidence_links": exp.evidence_links,
        } if exp else None

    async def _get_sources(self, prediction_id: int) -> List[dict]:
        stmt = select(PredictionSource).where(PredictionSource.prediction_id == prediction_id)
        result = await self.db.execute(stmt)
        return [
            {"source_type": s.source_type, "source_id": s.source_id,
             "source_name": s.source_name, "relevance_score": s.relevance_score}
            for s in result.scalars().all()
        ]

    async def _explanation_exists(self, prediction_id: int) -> Optional[PredictionExplanationRecord]:
        stmt = select(PredictionExplanationRecord).where(
            PredictionExplanationRecord.prediction_id == prediction_id
        )
        result = await self.db.execute(stmt)
        return result.scalar()

    async def _source_exists(self, prediction_id: int, source_type: str, source_id: int) -> Optional[PredictionSource]:
        stmt = select(PredictionSource).where(
            PredictionSource.prediction_id == prediction_id,
            PredictionSource.source_type == source_type,
            PredictionSource.source_id == source_id,
        )
        result = await self.db.execute(stmt)
        return result.scalar()
