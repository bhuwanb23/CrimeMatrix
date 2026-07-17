from typing import Dict, List
import structlog

logger = structlog.get_logger()


class CrimeForecasting:
    def forecast(self, historical_data: List[Dict], periods_ahead: int = 1) -> Dict:
        if not historical_data:
            return {"predictions": [], "trend": "insufficient_data", "confidence": 0}

        counts = [d.get("count", 0) for d in historical_data]
        if len(counts) < 2:
            return {"predictions": [{"period": "next", "count": counts[0]}], "trend": "stable", "confidence": 30}

        n = len(counts)
        avg = sum(counts) / n
        recent_avg = sum(counts[-3:]) / min(3, n)

        if n >= 3:
            slope = (counts[-1] - counts[-3]) / 2
        else:
            slope = counts[-1] - counts[0]

        predictions = []
        for i in range(1, periods_ahead + 1):
            predicted = recent_avg + (slope * i)
            predicted = max(0, round(predicted))
            predictions.append({"period": f"next_{i}", "count": predicted})

        trend = "increasing" if slope > 0.5 else "decreasing" if slope < -0.5 else "stable"

        variance = sum((x - avg) ** 2 for x in counts) / n
        consistency = max(0, 100 - variance * 2)
        confidence = min(100, max(10, int(consistency + len(counts) * 5)))

        return {
            "predictions": predictions,
            "trend": trend,
            "trend_slope": round(slope, 2),
            "current_average": round(avg, 1),
            "confidence": confidence,
            "data_points": n,
        }

    def detect_anomalies(self, data: List[Dict], threshold: float = 2.0) -> List[Dict]:
        if len(data) < 3:
            return []
        counts = [d.get("count", 0) for d in data]
        avg = sum(counts) / len(counts)
        std = (sum((x - avg) ** 2 for x in counts) / len(counts)) ** 0.5
        if std == 0:
            return []

        anomalies = []
        for i, d in enumerate(data):
            z_score = (d.get("count", 0) - avg) / std
            if abs(z_score) > threshold:
                anomalies.append({**d, "z_score": round(z_score, 2), "type": "spike" if z_score > 0 else "dip"})
        return anomalies
