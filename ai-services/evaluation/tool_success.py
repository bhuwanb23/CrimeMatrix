from typing import Dict, List
from collections import defaultdict
from datetime import datetime
import structlog

logger = structlog.get_logger()


class ToolSuccessRate:
    def __init__(self):
        self._records: List[dict] = []

    def record(self, tool_name: str, success: bool, duration_ms: float = 0,
               error: str = None):
        entry = {
            "tool": tool_name,
            "success": success,
            "duration_ms": round(duration_ms, 2),
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }
        self._records.append(entry)
        if len(self._records) > 10000:
            self._records = self._records[-10000:]

    def get_stats(self, tool_name: str = None) -> Dict:
        records = self._records
        if tool_name:
            records = [r for r in records if r["tool"] == tool_name]

        if not records:
            return {"total": 0, "success": 0, "failure": 0, "success_rate": 0}

        success = sum(1 for r in records if r["success"])
        total = len(records)

        return {
            "total": total,
            "success": success,
            "failure": total - success,
            "success_rate": round(success / total * 100, 1) if total > 0 else 0,
            "avg_duration_ms": round(sum(r["duration_ms"] for r in records) / total, 2) if total else 0,
        }

    def get_by_tool(self) -> Dict[str, Dict]:
        by_tool = defaultdict(list)
        for r in self._records:
            by_tool[r["tool"]].append(r)

        result = {}
        for tool, records in by_tool.items():
            success = sum(1 for r in records if r["success"])
            total = len(records)
            result[tool] = {
                "total": total,
                "success": success,
                "success_rate": round(success / total * 100, 1) if total else 0,
            }
        return result

    def get_errors(self, limit: int = 20) -> List[dict]:
        errors = [r for r in self._records if not r["success"]]
        return list(reversed(errors))[:limit]
