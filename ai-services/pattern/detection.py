from typing import List, Dict
from collections import defaultdict
from prediction.mo_similarity import MOSimilarity
import structlog

logger = structlog.get_logger()

MO_KEYWORDS = {
    "entry": ["break", "window", "door", "lock", "force", "pry", "drill"],
    "time": ["night", "morning", "evening", "dawn", "dusk", "late", "early"],
    "weapon": ["knife", "gun", "weapon", "threat", "force", "violence"],
    "target": ["jewelry", "cash", "electronics", "vehicle", "phone", "wallet"],
    "method": ["snatch", "grab", "con", "trick", "ambush", "distraction"],
    "transport": ["bike", "car", "walk", "bus", "auto", "escape"],
}

TIME_PERIODS = {
    "night_0_4": (0, 4, "Night (12 AM - 4 AM)"),
    "early_morning_4_8": (4, 8, "Early Morning (4 AM - 8 AM)"),
    "morning_8_12": (8, 12, "Morning (8 AM - 12 PM)"),
    "afternoon_12_16": (12, 16, "Afternoon (12 PM - 4 PM)"),
    "evening_16_20": (16, 20, "Evening (4 PM - 8 PM)"),
    "late_night_20_24": (20, 24, "Late Night (8 PM - 12 AM)"),
}


class PatternDetectionEngine:
    def __init__(self):
        self.mo_engine = MOSimilarity()

    def detect_all(self, crimes: List[Dict]) -> Dict:
        time_patterns = self.detect_time_patterns(crimes)
        mo_patterns = self.detect_mo_patterns(crimes)
        location_patterns = self.detect_location_patterns(crimes)
        type_patterns = self.detect_type_patterns(crimes)

        all_patterns = time_patterns + mo_patterns + location_patterns + type_patterns
        clusters = self.cluster_patterns(all_patterns)

        return {
            "time_patterns": time_patterns,
            "mo_patterns": mo_patterns,
            "location_patterns": location_patterns,
            "type_patterns": type_patterns,
            "all_patterns": all_patterns,
            "clusters": clusters,
            "total": len(all_patterns),
        }

    def detect_time_patterns(self, crimes: List[Dict]) -> List[Dict]:
        period_groups = defaultdict(list)
        for c in crimes:
            hour = self._get_hour(c)
            if hour is None:
                continue
            for period_key, (start, end, label) in TIME_PERIODS.items():
                if start <= hour < end:
                    period_groups[period_key].append(c)
                    break

        patterns = []
        for period_key, period_crimes in period_groups.items():
            if len(period_crimes) >= 3:
                _, _, label = TIME_PERIODS[period_key]
                confidence = min(100, len(period_crimes) * 12)
                patterns.append({
                    "name": f"{label} Crime Cluster",
                    "pattern_type": "time",
                    "time_pattern": period_key,
                    "description": f"{len(period_crimes)} crimes during {label.lower()}",
                    "confidence": confidence,
                    "frequency": len(period_crimes),
                    "crime_ids": [c.get("id") for c in period_crimes],
                })

        return patterns

    def detect_mo_patterns(self, crimes: List[Dict]) -> List[Dict]:
        category_groups = defaultdict(list)
        for c in crimes:
            desc = (c.get("description") or "").lower()
            if not desc:
                continue
            cats = set()
            for cat, keywords in MO_KEYWORDS.items():
                if any(kw in desc for kw in keywords):
                    cats.add(cat)
            if cats:
                category_groups[frozenset(cats)].append(c)

        patterns = []
        for categories, group_crimes in category_groups.items():
            if len(group_crimes) >= 3:
                cat_names = sorted(categories)
                confidence = min(100, len(group_crimes) * 15)
                patterns.append({
                    "name": f"MO Pattern: {', '.join(cat_names[:3])}",
                    "pattern_type": "mo",
                    "mo_summary": ", ".join(cat_names),
                    "description": f"{len(group_crimes)} crimes share MO: {', '.join(cat_names)}",
                    "confidence": confidence,
                    "frequency": len(group_crimes),
                    "crime_ids": [c.get("id") for c in group_crimes],
                })

        return patterns

    def detect_location_patterns(self, crimes: List[Dict]) -> List[Dict]:
        district_groups = defaultdict(list)
        for c in crimes:
            did = c.get("district_id")
            if did:
                district_groups[did].append(c)

        patterns = []
        for district_id, group_crimes in district_groups.items():
            if len(group_crimes) >= 3:
                confidence = min(100, len(group_crimes) * 10)
                patterns.append({
                    "name": f"Location Cluster: District #{district_id}",
                    "pattern_type": "location",
                    "location_pattern": f"district_{district_id}",
                    "description": f"{len(group_crimes)} crimes in district #{district_id}",
                    "confidence": confidence,
                    "frequency": len(group_crimes),
                    "crime_ids": [c.get("id") for c in group_crimes],
                })

        return patterns

    def detect_type_patterns(self, crimes: List[Dict]) -> List[Dict]:
        type_groups = defaultdict(list)
        for c in crimes:
            ct = c.get("crime_type_id")
            if ct:
                type_groups[ct].append(c)

        patterns = []
        for crime_type_id, group_crimes in type_groups.items():
            if len(group_crimes) >= 5:
                confidence = min(100, len(group_crimes) * 8)
                patterns.append({
                    "name": f"Type Cluster: Crime Type #{crime_type_id}",
                    "pattern_type": "type",
                    "description": f"{len(group_crimes)} crimes of type #{crime_type_id}",
                    "confidence": confidence,
                    "frequency": len(group_crimes),
                    "crime_ids": [c.get("id") for c in group_crimes],
                })

        return patterns

    def cluster_patterns(self, patterns: List[Dict]) -> List[Dict]:
        if not patterns:
            return []

        type_clusters = defaultdict(list)
        for p in patterns:
            type_clusters[p.get("pattern_type", "unknown")].append(p)

        clusters = []
        for ptype, group in type_clusters.items():
            if len(group) >= 2:
                pattern_ids = [str(i) for i in range(len(group))]
                clusters.append({
                    "name": f"{ptype.title()} Patterns Cluster",
                    "cluster_type": ptype,
                    "pattern_count": len(group),
                    "strength": sum(p.get("confidence", 0) for p in group) / len(group),
                    "description": f"{len(group)} related {ptype} patterns detected",
                })

        return clusters

    def _get_hour(self, crime: Dict) -> int:
        from datetime import datetime
        dt = crime.get("occurred_at") or crime.get("created_at")
        if not dt:
            return None
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except Exception:
                return None
        return dt.hour if hasattr(dt, "hour") else None
