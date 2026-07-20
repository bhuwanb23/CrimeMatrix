import json
from typing import Optional, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func as sql_func
from app.models.crime import Crime
from app.models.district import District
from app.models.crimetype import CrimeType
from app.models.crime_prediction import CrimePrediction
from app.models.prediction_model import PredictionModelRecord
from app.models.prediction_result import PredictionResult
import structlog
from datetime import datetime, timedelta
from collections import defaultdict

logger = structlog.get_logger()


class PredictionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def forecast(self, district_id: int = None, crime_type_id: int = None,
                       periods: int = 30) -> dict:
        # Get historical crime counts
        date_from = datetime.utcnow() - timedelta(days=periods * 2)
        query = select(
            sql_func.date(Crime.created_at).label("date"),
            sql_func.count(Crime.id).label("count")
        ).where(Crime.created_at >= date_from)
        if district_id:
            query = query.where(Crime.district_id == district_id)
        if crime_type_id:
            query = query.where(Crime.crime_type_id == crime_type_id)
        query = query.group_by(sql_func.date(Crime.created_at)).order_by(sql_func.date(Crime.created_at))
        result = await self.db.execute(query)
        data = [{"date": str(r[0]) if r[0] else "unknown", "count": r[1]} for r in result.all()]

        # Simple moving average forecast
        if len(data) < 2:
            forecast_data = []
            confidence = 10
        else:
            counts = [d["count"] for d in data]
            recent = counts[-7:] if len(counts) >= 7 else counts
            avg = sum(recent) / len(recent)
            earlier = counts[:7] if len(counts) >= 7 else counts
            earlier_avg = sum(earlier) / len(earlier)
            slope = (avg - earlier_avg) / max(len(earlier), 1)

            forecast_data = []
            for i in range(1, periods + 1):
                predicted = max(0, round(avg + slope * i))
                forecast_data.append({
                    "day": i,
                    "date": (datetime.utcnow() + timedelta(days=i)).strftime("%Y-%m-%d"),
                    "predicted": predicted,
                })

            variance = sum((x - avg) ** 2 for x in counts) / len(counts)
            confidence = min(100, max(10, int(80 - variance * 2)))

        # Save predictions
        for f in forecast_data:
            pred = CrimePrediction(
                prediction_type="forecast",
                district_id=district_id,
                crime_type_id=crime_type_id,
                predicted_value=f["predicted"],
                confidence=confidence,
                target_date=f["date"],
                model_name="moving_average",
                model_version="1.0",
                features_json=json.dumps({"periods": periods, "data_points": len(data)}),
            )
            self.db.add(pred)
        await self.db.commit()

        trend = "increasing" if len(data) >= 2 and data[-1]["count"] > data[0]["count"] else "decreasing" if len(data) >= 2 and data[-1]["count"] < data[0]["count"] else "stable"

        return {
            "historical": data,
            "forecast": forecast_data,
            "trend": trend,
            "confidence": confidence,
            "data_points": len(data),
        }

    async def get_predictions(self, prediction_type: str = None,
                               district_id: int = None) -> List[dict]:
        stmt = select(CrimePrediction)
        if prediction_type:
            stmt = stmt.where(CrimePrediction.prediction_type == prediction_type)
        if district_id:
            stmt = stmt.where(CrimePrediction.district_id == district_id)
        stmt = stmt.order_by(CrimePrediction.created_at.desc()).limit(100)
        result = await self.db.execute(stmt)
        return [self._prediction_to_dict(p) for p in result.scalars().all()]

    async def get_prediction(self, prediction_id: int) -> Optional[dict]:
        stmt = select(CrimePrediction).where(CrimePrediction.id == prediction_id)
        result = await self.db.execute(stmt)
        p = result.scalar()
        return self._prediction_to_dict(p) if p else None

    async def get_district_predictions(self, district_id: int) -> dict:
        stmt = select(CrimePrediction).where(
            CrimePrediction.district_id == district_id,
            CrimePrediction.prediction_type == "forecast",
        ).order_by(CrimePrediction.created_at.desc()).limit(30)
        result = await self.db.execute(stmt)
        predictions = [self._prediction_to_dict(p) for p in result.scalars().all()]

        district = await self._load_district(district_id)
        return {
            "district": district,
            "predictions": predictions,
            "total": len(predictions),
        }

    async def get_models(self) -> List[dict]:
        stmt = select(PredictionModelRecord).order_by(PredictionModelRecord.created_at.desc())
        result = await self.db.execute(stmt)
        return [self._model_to_dict(m) for m in result.scalars().all()]

    async def get_stats(self) -> dict:
        total = (await self.db.execute(select(sql_func.count(CrimePrediction.id)))).scalar() or 0
        forecasts = (await self.db.execute(
            select(sql_func.count(CrimePrediction.id)).where(CrimePrediction.prediction_type == "forecast")
        )).scalar() or 0
        avg_conf = (await self.db.execute(select(sql_func.avg(CrimePrediction.confidence)))).scalar()
        models = (await self.db.execute(select(sql_func.count(PredictionModelRecord.id)))).scalar() or 0

        return {
            "total_predictions": total,
            "forecasts": forecasts,
            "avg_confidence": round(avg_conf or 0, 1),
            "total_models": models,
        }

    async def _load_district(self, district_id: int) -> Optional[dict]:
        stmt = select(District).where(District.id == district_id)
        result = await self.db.execute(stmt)
        d = result.scalar()
        return {"id": d.id, "name": d.name} if d else None

    def _prediction_to_dict(self, p: CrimePrediction) -> dict:
        return {
            "id": p.id, "prediction_type": p.prediction_type,
            "district_id": p.district_id, "crime_type_id": p.crime_type_id,
            "predicted_value": p.predicted_value, "confidence": p.confidence,
            "actual_value": p.actual_value, "target_date": p.target_date,
            "model_name": p.model_name, "status": p.status,
            "created_at": str(p.created_at) if p.created_at else None,
        }

    def _model_to_dict(self, m: PredictionModelRecord) -> dict:
        return {
            "id": m.id, "name": m.name, "version": m.version,
            "accuracy": m.accuracy, "status": m.status,
            "last_trained": str(m.last_trained) if m.last_trained else None,
        }
