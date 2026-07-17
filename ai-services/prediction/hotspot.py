from typing import Dict, List
import structlog

logger = structlog.get_logger()


class HotspotPrediction:
    def identify_hotspots(self, crime_data: List[Dict], top_n: int = 5) -> List[Dict]:
        location_counts = {}
        for crime in crime_data:
            loc = crime.get("district") or crime.get("location") or "unknown"
            if loc not in location_counts:
                location_counts[loc] = {"count": 0, "types": {}, "recent": 0}
            location_counts[loc]["count"] += 1
            ct = crime.get("crime_type", "unknown")
            location_counts[loc]["types"][ct] = location_counts[loc]["types"].get(ct, 0) + 1

        hotspots = []
        for loc, data in location_counts.items():
            density = data["count"]
            dominant_type = max(data["types"], key=data["types"].get) if data["types"] else "unknown"
            risk_level = "critical" if density > 20 else "high" if density > 10 else "medium" if density > 5 else "low"
            hotspots.append({
                "location": loc,
                "crime_count": density,
                "dominant_type": dominant_type,
                "risk_level": risk_level,
                "type_distribution": data["types"],
            })

        hotspots.sort(key=lambda x: x["crime_count"], reverse=True)
        return hotspots[:top_n]

    def hotspot_trend(self, location: str, crime_data: List[Dict]) -> Dict:
        location_crimes = [c for c in crime_data if c.get("district") == location or c.get("location") == location]
        if len(location_crimes) < 2:
            return {"location": location, "trend": "insufficient_data", "count": len(location_crimes)}

        counts_by_period = {}
        for c in location_crimes:
            period = c.get("period", c.get("created_at", "unknown"))[:7]
            counts_by_period[period] = counts_by_period.get(period, 0) + 1

        periods = sorted(counts_by_period.keys())
        if len(periods) < 2:
            return {"location": location, "trend": "stable", "count": len(location_crimes)}

        recent = counts_by_period[periods[-1]]
        previous = counts_by_period[periods[-2]]
        change = ((recent - previous) / previous * 100) if previous > 0 else 0

        trend = "worsening" if change > 20 else "improving" if change < -20 else "stable"
        return {
            "location": location,
            "trend": trend,
            "change_percent": round(change, 1),
            "recent_count": recent,
            "previous_count": previous,
        }
