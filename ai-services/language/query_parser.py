import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from core.provider import registry as provider_registry
import structlog

logger = structlog.get_logger()

CRIME_TYPES = ["theft", "murder", "robbery", "fraud", "assault", "burglary", "kidnapping",
               "drug", "cybercrime", "domestic violence", "hit and run", "vehicle theft",
               "snatching", "extortion", "forgery", "cheating"]

DISTRICTS = ["bengaluru", "bangalore", "mysore", "mysuru", "hubli", "dharwad", "mangalore",
             "mangaluru", "belgaum", "belagavi", "gulbarga", "kalaburagi", "bijapur",
             "vijayapura", " Shimoga", "shivamogga", "davangere", "raichur", "bellary",
             "ballari", "hassan", "mandya", "tumkur", "tumakuru", "kolar", "chikkaballapur",
             "ramnagar", "chamarajanagar", "kodagu", "coorg", "uttara kannada", "dakshina kannada",
             "Udupi", "chitradurga", "davanagere"]

STATUS_KEYWORDS = {"open": "open", "closed": "closed", "pending": "pending",
                   "active": "active", "resolved": "closed", "solved": "closed",
                   "under investigation": "active", "filed": "open"}

PRIORITY_KEYWORDS = {"high": "high", "critical": "high", "urgent": "high",
                     "medium": "medium", "low": "low", "minor": "low"}


class NLQueryParser:
    def __init__(self):
        self._compiled_patterns = self._build_patterns()

    def _build_patterns(self) -> Dict:
        return {
            "crime_type": [(kw, kw) for kw in CRIME_TYPES],
            "district": [(kw, kw) for kw in DISTRICTS],
            "status": [(kw, val) for kw, val in STATUS_KEYWORDS.items()],
            "priority": [(kw, val) for kw, val in PRIORITY_KEYWORDS.items()],
        }

    def parse(self, query: str) -> Dict:
        query_lower = query.lower().strip()
        filters = {}

        # Extract crime type
        for keyword, value in self._compiled_patterns["crime_type"]:
            if keyword in query_lower:
                filters["crime_type"] = value
                break

        # Extract district
        for keyword, value in self._compiled_patterns["district"]:
            if keyword in query_lower:
                filters["district"] = value
                break

        # Extract status
        for keyword, value in self._compiled_patterns["status"]:
            if keyword in query_lower:
                filters["status"] = value
                break

        # Extract priority
        for keyword, value in self._compiled_patterns["priority"]:
            if keyword in query_lower:
                filters["priority"] = value
                break

        # Extract date ranges
        date_filter = self._extract_date_range(query_lower)
        if date_filter:
            filters.update(date_filter)

        # Extract numeric limits
        limit = self._extract_limit(query_lower)
        if limit:
            filters["limit"] = limit

        return {
            "query": query,
            "filters": filters,
            "has_filters": len(filters) > 0,
        }

    def _extract_date_range(self, query: str) -> Dict:
        now = datetime.now()

        # "last N days/weeks/months"
        match = re.search(r'last\s+(\d+)\s+(day|week|month|year)s?', query)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if unit == "day":
                start = now - timedelta(days=num)
            elif unit == "week":
                start = now - timedelta(weeks=num)
            elif unit == "month":
                start = now - timedelta(days=num * 30)
            elif unit == "year":
                start = now - timedelta(days=num * 365)
            else:
                return {}
            return {"date_from": start.strftime("%Y-%m-%d"), "date_to": now.strftime("%Y-%m-%d")}

        # "yesterday"
        if "yesterday" in query:
            yesterday = now - timedelta(days=1)
            return {"date_from": yesterday.strftime("%Y-%m-%d"), "date_to": yesterday.strftime("%Y-%m-%d")}

        # "today"
        if "today" in query:
            return {"date_from": now.strftime("%Y-%m-%d"), "date_to": now.strftime("%Y-%m-%d")}

        # "this week"
        if "this week" in query:
            start = now - timedelta(days=now.weekday())
            return {"date_from": start.strftime("%Y-%m-%d"), "date_to": now.strftime("%Y-%m-%d")}

        # "this month"
        if "this month" in query:
            start = now.replace(day=1)
            return {"date_from": start.strftime("%Y-%m-%d"), "date_to": now.strftime("%Y-%m-%d")}

        # "between X and Y"
        match = re.search(r'between\s+(\w+\s+\d+)\s+and\s+(\w+\s+\d+)', query)
        if match:
            try:
                start = datetime.strptime(match.group(1), "%B %d")
                end = datetime.strptime(match.group(2), "%B %d")
                start = start.replace(year=now.year)
                end = end.replace(year=now.year)
                return {"date_from": start.strftime("%Y-%m-%d"), "date_to": end.strftime("%Y-%m-%d")}
            except ValueError:
                pass

        return {}

    def _extract_limit(self, query: str) -> Optional[int]:
        match = re.search(r'(?:top|first|show|get)\s+(\d+)', query)
        if match:
            return int(match.group(1))
        return None


query_parser = NLQueryParser()
