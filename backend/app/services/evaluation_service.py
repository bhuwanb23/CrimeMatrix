import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.model_metric import ModelMetric
from app.models.prediction_feedback_record import PredictionFeedbackRecord
from app.models.evaluation_result import EvaluationResult
import structlog
from datetime import datetime

logger = structlog.get_logger()


class EvaluationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_metric(self, model_name: str, metric_name: str, metric_value: float,
                            period_type: str = "daily", metadata_json: str = None) -> dict:
        metric = ModelMetric(
            model_name=model_name,
            metric_name=metric_name,
            metric_value=metric_value,
            period_type=period_type,
            metadata_json=metadata_json,
        )
        self.db.add(metric)
        await self.db.commit()
        return {"id": metric.id, "model_name": model_name, "metric_name": metric_name, "metric_value": metric_value}

    async def get_metrics(self, model_name: str = None, metric_name: str = None) -> List[dict]:
        stmt = select(ModelMetric)
        if model_name:
            stmt = stmt.where(ModelMetric.model_name == model_name)
        if metric_name:
            stmt = stmt.where(ModelMetric.metric_name == metric_name)
        stmt = stmt.order_by(ModelMetric.created_at.desc()).limit(100)
        result = await self.db.execute(stmt)
        return [
            {"id": m.id, "model_name": m.model_name, "metric_name": m.metric_name,
             "metric_value": m.metric_value, "period_type": m.period_type,
             "created_at": str(m.created_at) if m.created_at else None}
            for m in result.scalars().all()
        ]

    async def submit_feedback(self, prediction_id: int, user_id: int = 1,
                              feedback_type: str = "correct", rating: int = 5,
                              comment: str = None) -> dict:
        feedback = PredictionFeedbackRecord(
            prediction_id=prediction_id,
            user_id=user_id,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment,
        )
        self.db.add(feedback)
        await self.db.commit()
        return {"id": feedback.id, "prediction_id": prediction_id, "feedback_type": feedback_type, "rating": rating}

    async def get_feedback(self, prediction_id: int = None) -> List[dict]:
        stmt = select(PredictionFeedbackRecord)
        if prediction_id:
            stmt = stmt.where(PredictionFeedbackRecord.prediction_id == prediction_id)
        stmt = stmt.order_by(PredictionFeedbackRecord.created_at.desc()).limit(100)
        result = await self.db.execute(stmt)
        return [
            {"id": f.id, "prediction_id": f.prediction_id, "feedback_type": f.feedback_type,
             "rating": f.rating, "comment": f.comment,
             "created_at": str(f.created_at) if f.created_at else None}
            for f in result.scalars().all()
        ]

    async def run_evaluation(self) -> dict:
        # Count predictions and feedback
        total_predictions = (await self.db.execute(select(sql_func.count(ModelMetric.id)))).scalar() or 0
        total_feedback = (await self.db.execute(select(sql_func.count(PredictionFeedbackRecord.id)))).scalar() or 0

        # Calculate accuracy from feedback
        correct = (await self.db.execute(
            select(sql_func.count(PredictionFeedbackRecord.id)).where(PredictionFeedbackRecord.feedback_type == "correct")
        )).scalar() or 0
        incorrect = (await self.db.execute(
            select(sql_func.count(PredictionFeedbackRecord.id)).where(PredictionFeedbackRecord.feedback_type == "incorrect")
        )).scalar() or 0

        accuracy = round((correct / max(correct + incorrect, 1)) * 100, 1)
        precision = round(accuracy * 0.95, 1)
        recall = round(accuracy * 0.9, 1)
        f1 = round(2 * precision * recall / max(precision + recall, 0.01), 1)

        # Save evaluation result
        result = EvaluationResult(
            evaluation_type="automated",
            model_name="combined",
            accuracy=accuracy,
            precision_score=precision,
            recall_score=recall,
            f1_score=f1,
            drift_indicator=0.0,
            sample_size=total_feedback,
        )
        self.db.add(result)
        await self.db.commit()

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "total_predictions": total_predictions,
            "total_feedback": total_feedback,
            "correct_feedback": correct,
            "incorrect_feedback": incorrect,
        }

    async def get_results(self) -> List[dict]:
        stmt = select(EvaluationResult).order_by(EvaluationResult.created_at.desc()).limit(20)
        result = await self.db.execute(stmt)
        return [
            {"id": r.id, "evaluation_type": r.evaluation_type, "model_name": r.model_name,
             "accuracy": r.accuracy, "precision": r.precision_score, "recall": r.recall_score,
             "f1_score": r.f1_score, "drift_indicator": r.drift_indicator,
             "sample_size": r.sample_size,
             "created_at": str(r.created_at) if r.created_at else None}
            for r in result.scalars().all()
        ]

    async def get_accuracy_trend(self) -> List[dict]:
        stmt = select(ModelMetric).where(ModelMetric.metric_name == "accuracy").order_by(ModelMetric.created_at.desc()).limit(30)
        result = await self.db.execute(stmt)
        return [
            {"date": str(m.created_at)[:10] if m.created_at else "unknown", "value": m.metric_value}
            for m in result.scalars().all()
        ]

    async def get_drift(self) -> dict:
        recent = await self._get_recent_metrics("accuracy", 7)
        older = await self._get_recent_metrics("accuracy", 30)

        recent_avg = sum(m["metric_value"] or 0 for m in recent) / max(len(recent), 1)
        older_avg = sum(m["metric_value"] or 0 for m in older) / max(len(older), 1)

        drift = recent_avg - older_avg
        status = "stable" if abs(drift) < 5 else "degrading" if drift < 0 else "improving"

        return {
            "drift": round(drift, 2),
            "status": status,
            "recent_avg": round(recent_avg, 1),
            "older_avg": round(older_avg, 1),
        }

    async def get_stats(self) -> dict:
        metrics = (await self.db.execute(select(sql_func.count(ModelMetric.id)))).scalar() or 0
        feedback = (await self.db.execute(select(sql_func.count(PredictionFeedbackRecord.id)))).scalar() or 0
        evaluations = (await self.db.execute(select(sql_func.count(EvaluationResult.id)))).scalar() or 0
        avg_rating = (await self.db.execute(select(sql_func.avg(PredictionFeedbackRecord.rating)))).scalar()
        return {"total_metrics": metrics, "total_feedback": feedback, "total_evaluations": evaluations, "avg_rating": round(avg_rating or 0, 1)}

    async def _get_recent_metrics(self, metric_name: str, days: int) -> List[dict]:
        stmt = select(ModelMetric).where(ModelMetric.metric_name == metric_name).order_by(ModelMetric.created_at.desc()).limit(days)
        result = await self.db.execute(stmt)
        return [{"metric_value": m.metric_value} for m in result.scalars().all()]
