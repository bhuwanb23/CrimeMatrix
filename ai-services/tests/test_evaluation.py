import pytest
from evaluation.latency import LatencyTracker
from evaluation.tokens import TokenTracker
from evaluation.hallucination import HallucinationDetector
from evaluation.tool_success import ToolSuccessRate
from evaluation.accuracy import AccuracyTracker
from evaluation.confidence import ConfidenceTracker
from evaluation.cost import CostTracker
from evaluation.feedback import FeedbackLoop
from evaluation.dashboard import MonitoringDashboard


class TestLatencyTracker:
    def setup_method(self):
        self.tracker = LatencyTracker()

    def test_record_latency(self):
        self.tracker.start("req1")
        import time; time.sleep(0.01)
        duration = self.tracker.end("req1", "/chat", "ollama")
        assert duration > 0

    def test_stats(self):
        self.tracker._records = [
            {"duration_ms": 100, "endpoint": "/chat", "provider": "ollama", "request_id": "r1", "timestamp": "2024-01-01"},
            {"duration_ms": 200, "endpoint": "/chat", "provider": "ollama", "request_id": "r2", "timestamp": "2024-01-01"},
            {"duration_ms": 150, "endpoint": "/chat", "provider": "ollama", "request_id": "r3", "timestamp": "2024-01-01"},
        ]
        stats = self.tracker.get_stats()
        assert stats["count"] == 3
        assert stats["avg_ms"] > 0

    def test_slow_requests(self):
        self.tracker._records.append({"duration_ms": 10000, "endpoint": "/chat"})
        slow = self.tracker.get_slow_requests(threshold_ms=5000)
        assert len(slow) == 1


class TestTokenTracker:
    def setup_method(self):
        self.tracker = TokenTracker()

    def test_record(self):
        self.tracker.record("ollama", "llama3.2:1b", 100, 50)
        stats = self.tracker.get_stats()
        assert stats["total_calls"] == 1
        assert stats["total_tokens"] == 150

    def test_by_provider(self):
        self.tracker.record("ollama", "llama3.2:1b", 100, 50)
        self.tracker.record("openai", "gpt-4o", 200, 100)
        by_prov = self.tracker.get_by_provider()
        assert "ollama" in by_prov
        assert "openai" in by_prov


class TestHallucinationDetector:
    def setup_method(self):
        self.detector = HallucinationDetector()

    def test_clean_response(self):
        evidence = [{"content": "Theft at MG Road, Bengaluru"}]
        result = self.detector.check("Theft occurred at MG Road.", evidence)
        assert result["verdict"] == "clean"

    def test_no_evidence(self):
        result = self.detector.check("The sky is blue.", [])
        assert result["total_claims"] > 0

    def test_stats(self):
        self.detector.check("Test response", [{"content": "test"}])
        stats = self.detector.get_stats()
        assert stats["total_checks"] == 1


class TestToolSuccessRate:
    def setup_method(self):
        self.tracker = ToolSuccessRate()

    def test_record_success(self):
        self.tracker.record("calculator", True, 50)
        stats = self.tracker.get_stats("calculator")
        assert stats["success_rate"] == 100

    def test_record_failure(self):
        self.tracker.record("calculator", True, 50)
        self.tracker.record("calculator", False, 100, error="timeout")
        stats = self.tracker.get_stats("calculator")
        assert stats["success_rate"] == 50

    def test_by_tool(self):
        self.tracker.record("calc", True, 10)
        self.tracker.record("search", False, 100)
        by_tool = self.tracker.get_by_tool()
        assert by_tool["calc"]["success_rate"] == 100
        assert by_tool["search"]["success_rate"] == 0


class TestAccuracyTracker:
    def setup_method(self):
        self.tracker = AccuracyTracker()

    def test_record(self):
        self.tracker.record("query", "response", 85, "crime")
        stats = self.tracker.get_stats()
        assert stats["avg_accuracy"] == 85

    def test_by_domain(self):
        self.tracker.record("q", "r", 90, "crime")
        self.tracker.record("q", "r", 70, "identity")
        by_domain = self.tracker.get_by_domain()
        assert by_domain["crime"]["avg_accuracy"] == 90


class TestConfidenceTracker:
    def setup_method(self):
        self.tracker = ConfidenceTracker()

    def test_distribution(self):
        for c in [10, 30, 50, 70, 90]:
            self.tracker.record(c)
        dist = self.tracker.get_distribution()
        assert dist["count"] == 5

    def test_calibration(self):
        self.tracker.record(80, was_correct=True)
        self.tracker.record(80, was_correct=True)
        self.tracker.record(80, was_correct=False)
        cal = self.tracker.get_calibration()
        assert len(cal["calibration_data"]) > 0


class TestCostTracker:
    def setup_method(self):
        self.tracker = CostTracker()

    def test_ollama_free(self):
        self.tracker.record("ollama", "llama3.2:1b", 100, 50)
        stats = self.tracker.get_stats()
        assert stats["total_cost_usd"] == 0

    def test_openai_cost(self):
        self.tracker.record("openai", "gpt-4o-mini", 1000, 500)
        stats = self.tracker.get_stats()
        assert stats["total_cost_usd"] > 0

    def test_by_provider(self):
        self.tracker.record("ollama", "llama3.2:1b", 100, 50)
        self.tracker.record("openai", "gpt-4o", 1000, 500)
        by_prov = self.tracker.get_by_provider()
        assert by_prov["ollama"]["cost_usd"] == 0
        assert by_prov["openai"]["cost_usd"] > 0


class TestFeedbackLoop:
    def setup_method(self):
        self.loop = FeedbackLoop()

    def test_submit(self):
        self.loop.submit(5, "great response", "thanks")
        stats = self.loop.get_stats()
        assert stats["total"] == 1
        assert stats["avg_rating"] == 5

    def test_distribution(self):
        for r in [1, 2, 3, 4, 5]:
            self.loop.submit(r, "query")
        stats = self.loop.get_stats()
        assert stats["total"] == 5

    def test_negative_feedback(self):
        self.loop.submit(1, "bad", "terrible")
        negative = self.loop.get_negative_feedback()
        assert len(negative) == 1


class TestMonitoringDashboard:
    def setup_method(self):
        self.dashboard = MonitoringDashboard()

    def test_full_dashboard(self):
        data = self.dashboard.get_full_dashboard()
        assert "latency" in data
        assert "tokens" in data
        assert "feedback" in data

    def test_summary(self):
        summary = self.dashboard.get_summary()
        assert "total_requests" in summary
        assert "total_cost_usd" in summary

    def test_record_request(self):
        self.dashboard.record_request("/chat", "ollama", 100, 50, 25)
        assert self.dashboard.latency.get_stats()["count"] == 1
