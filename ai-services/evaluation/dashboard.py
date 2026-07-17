from datetime import datetime
from typing import Dict
from evaluation.latency import LatencyTracker
from evaluation.tokens import TokenTracker
from evaluation.hallucination import HallucinationDetector
from evaluation.tool_success import ToolSuccessRate
from evaluation.accuracy import AccuracyTracker
from evaluation.confidence import ConfidenceTracker
from evaluation.cost import CostTracker
from evaluation.feedback import FeedbackLoop
import structlog

logger = structlog.get_logger()


class MonitoringDashboard:
    def __init__(self):
        self.latency = LatencyTracker()
        self.tokens = TokenTracker()
        self.hallucination = HallucinationDetector()
        self.tool_success = ToolSuccessRate()
        self.accuracy = AccuracyTracker()
        self.confidence = ConfidenceTracker()
        self.cost = CostTracker()
        self.feedback = FeedbackLoop()

    def get_full_dashboard(self) -> Dict:
        return {
            "latency": self.latency.get_stats(),
            "tokens": self.tokens.get_stats(),
            "hallucination": self.hallucination.get_stats(),
            "tool_success": self.tool_success.get_stats(),
            "accuracy": self.accuracy.get_stats(),
            "confidence": self.confidence.get_stats(),
            "cost": self.cost.get_stats(),
            "feedback": self.feedback.get_stats(),
        }

    def get_summary(self) -> Dict:
        return {
            "total_requests": self.latency.get_stats().get("count", 0),
            "total_tokens": self.tokens.get_stats().get("total_tokens", 0),
            "hallucination_rate": self.hallucination.get_stats().get("avg_hallucination_rate", 0),
            "tool_success_rate": self.tool_success.get_stats().get("success_rate", 0),
            "avg_accuracy": self.accuracy.get_stats().get("avg_accuracy", 0),
            "avg_confidence": self.confidence.get_stats().get("avg_confidence", 0),
            "total_cost_usd": self.cost.get_stats().get("total_cost_usd", 0),
            "avg_feedback_rating": self.feedback.get_stats().get("avg_rating", 0),
        }

    def record_request(self, endpoint: str, provider: str, duration_ms: float,
                        prompt_tokens: int = 0, completion_tokens: int = 0,
                        success: bool = True, tool_name: str = None):
        req_id = f"req_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        self.latency._records.append({
            "request_id": req_id, "endpoint": endpoint, "provider": provider,
            "duration_ms": duration_ms, "timestamp": datetime.now().isoformat(),
        })
        if prompt_tokens > 0:
            self.tokens.record(provider, provider, prompt_tokens, completion_tokens)
        if tool_name:
            self.tool_success.record(tool_name, success, duration_ms)
