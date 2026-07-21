"""
Feature 4 — AI Analytics & Prediction: Pytest Unit Tests
Tests database models, services, and API endpoints.
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ============================================================
# Database Table Validation
# ============================================================

class TestDatabaseTables:
    """Verify all Feature 4 tables exist with correct columns."""

    def _check_table(self, table_name, expected_columns):
        import sqlite3
        conn = sqlite3.connect(r'D:\projects\website\crimematrix\backend\data\crimematrix.db')
        c = conn.cursor()
        c.execute(f"PRAGMA table_info({table_name})")
        columns = [r[1] for r in c.fetchall()]
        conn.close()
        for col in expected_columns:
            assert col in columns, f"Table {table_name} missing column: {col}"
        return True

    def test_crime_predictions_table(self):
        assert self._check_table('crime_predictions', [
            'id', 'prediction_type', 'district_id', 'crime_type_id',
            'predicted_value', 'confidence', 'target_date', 'model_name', 'status'
        ])

    def test_prediction_models_table(self):
        assert self._check_table('prediction_models', [
            'id', 'name', 'version', 'accuracy', 'status'
        ])

    def test_prediction_results_table(self):
        assert self._check_table('prediction_results', [
            'id', 'prediction_id', 'metric_name', 'expected_value', 'actual_value'
        ])

    def test_early_warning_alerts_table(self):
        assert self._check_table('early_warning_alerts', [
            'id', 'alert_type', 'title', 'severity', 'status', 'confidence'
        ])

    def test_alert_rules_table(self):
        assert self._check_table('alert_rules', [
            'id', 'name', 'rule_type', 'threshold', 'is_active'
        ])

    def test_alert_events_table(self):
        assert self._check_table('alert_events', [
            'id', 'alert_id', 'event_type', 'message', 'created_by'
        ])

    def test_suspect_risk_scores_table(self):
        assert self._check_table('suspect_risk_scores', [
            'id', 'suspect_id', 'overall_score', 'risk_level',
            'criminal_history_score', 'explanation_json'
        ])

    def test_risk_score_history_table(self):
        assert self._check_table('risk_score_history', [
            'id', 'suspect_id', 'score', 'risk_level', 'scored_at'
        ])

    def test_risk_factors_table(self):
        assert self._check_table('risk_factors', [
            'id', 'suspect_id', 'factor_name', 'factor_value', 'weight'
        ])

    def test_crime_forecasts_table(self):
        assert self._check_table('crime_forecasts', [
            'id', 'district_id', 'period', 'predicted_count', 'actual_count', 'confidence'
        ])

    def test_forecast_snapshots_table(self):
        assert self._check_table('forecast_snapshots', [
            'id', 'metric_name', 'metric_value', 'forecast_value', 'confidence'
        ])

    def test_case_priorities_table(self):
        assert self._check_table('case_priorities', [
            'id', 'investigation_id', 'overall_priority_score', 'priority_level'
        ])

    def test_priority_history_table(self):
        assert self._check_table('priority_history', [
            'id', 'investigation_id', 'priority_score', 'priority_level'
        ])

    def test_priority_explanations_table(self):
        assert self._check_table('priority_explanations', [
            'id', 'investigation_id', 'factor_name', 'factor_score', 'explanation'
        ])

    def test_prediction_explanations_table(self):
        assert self._check_table('prediction_explanations', [
            'id', 'prediction_id', 'explanation_type', 'contributing_factors', 'model_explanation'
        ])

    def test_prediction_sources_table(self):
        assert self._check_table('prediction_sources', [
            'id', 'prediction_id', 'source_type', 'source_name', 'relevance_score'
        ])

    def test_model_metrics_table(self):
        assert self._check_table('model_metrics', [
            'id', 'model_name', 'metric_name', 'metric_value', 'period_type'
        ])

    def test_prediction_feedback_table(self):
        assert self._check_table('prediction_feedback', [
            'id', 'prediction_id', 'feedback_type', 'rating', 'comment'
        ])

    def test_evaluation_results_table(self):
        assert self._check_table('evaluation_results', [
            'id', 'evaluation_type', 'model_name', 'accuracy', 'precision_score',
            'recall_score', 'f1_score', 'drift_indicator'
        ])


# ============================================================
# API Endpoint Tests
# ============================================================

class TestAnalyticsDashboardAPI:
    """Test AI Analytics Dashboard endpoints."""

    def test_summary(self):
        r = client.get("/api/v1/analytics-dashboard/summary")
        assert r.status_code == 200
        data = r.json()["data"]
        assert "overview" in data
        assert "intelligence" in data
        assert "predictions" in data

    def test_alerts(self):
        r = client.get("/api/v1/analytics-dashboard/alerts")
        assert r.status_code == 200

    def test_forecasts(self):
        r = client.get("/api/v1/analytics-dashboard/forecasts")
        assert r.status_code == 200

    def test_high_risk(self):
        r = client.get("/api/v1/analytics-dashboard/high-risk")
        assert r.status_code == 200

    def test_priority(self):
        r = client.get("/api/v1/analytics-dashboard/priority")
        assert r.status_code == 200


class TestPredictionAPI:
    """Test Predictive Analytics endpoints."""

    def test_stats(self):
        r = client.get("/api/v1/predictions/stats")
        assert r.status_code == 200
        assert "total_predictions" in r.json()["data"]

    def test_list_predictions(self):
        r = client.get("/api/v1/predictions/")
        assert r.status_code == 200

    def test_generate_forecast(self):
        r = client.post("/api/v1/predictions/forecast", json={"periods": 30})
        assert r.status_code == 200
        data = r.json()["data"]
        assert "forecast" in data or "predictions" in data

    def test_seasonal_patterns(self):
        r = client.get("/api/v1/predictions/forecast/seasonal?days=365")
        assert r.status_code == 200

    def test_forecast_stats(self):
        r = client.get("/api/v1/predictions/forecast/stats")
        assert r.status_code == 200


class TestEarlyWarningAPI:
    """Test Early Warning endpoints."""

    def test_stats(self):
        r = client.get("/api/v1/early-warning/stats")
        assert r.status_code == 200

    def test_list_alerts(self):
        r = client.get("/api/v1/early-warning/alerts")
        assert r.status_code == 200

    def test_detect_alerts(self):
        r = client.post("/api/v1/early-warning/detect")
        assert r.status_code == 200

    def test_rules(self):
        r = client.get("/api/v1/early-warning/rules")
        assert r.status_code == 200


class TestRiskScoringAPI:
    """Test Suspect Risk Scoring endpoints."""

    def test_stats(self):
        r = client.get("/api/v1/suspect-risk/stats")
        assert r.status_code == 200

    def test_rankings(self):
        r = client.get("/api/v1/suspect-risk/rankings?limit=5")
        assert r.status_code == 200

    def test_list_scores(self):
        r = client.get("/api/v1/suspect-risk/scores")
        assert r.status_code == 200


class TestPrioritizationAPI:
    """Test Case Prioritization endpoints."""

    def test_stats(self):
        r = client.get("/api/v1/priorities/stats")
        assert r.status_code == 200

    def test_rankings(self):
        r = client.get("/api/v1/priorities/rankings?limit=5")
        assert r.status_code == 200

    def test_workload(self):
        r = client.get("/api/v1/priorities/workload")
        assert r.status_code == 200


class TestExplanationAPI:
    """Test Explainable Predictions endpoints."""

    def test_explain_prediction(self):
        r = client.post("/api/v1/predictions/explain/1")
        assert r.status_code == 200

    def test_get_explanation(self):
        r = client.get("/api/v1/predictions/explain/1")
        assert r.status_code == 200

    def test_get_sources(self):
        r = client.get("/api/v1/predictions/sources/1")
        assert r.status_code == 200

    def test_confidence_breakdown(self):
        r = client.get("/api/v1/predictions/confidence/1")
        assert r.status_code == 200


class TestEvaluationAPI:
    """Test Model Evaluation endpoints."""

    def test_stats(self):
        r = client.get("/api/v1/evaluation/stats")
        assert r.status_code == 200

    def test_run_evaluation(self):
        r = client.post("/api/v1/evaluation/run")
        assert r.status_code == 200
        data = r.json()["data"]
        assert "accuracy" in data

    def test_metrics(self):
        r = client.get("/api/v1/evaluation/metrics")
        assert r.status_code == 200

    def test_feedback(self):
        r = client.get("/api/v1/evaluation/feedback")
        assert r.status_code == 200

    def test_accuracy_trend(self):
        r = client.get("/api/v1/evaluation/accuracy-trend")
        assert r.status_code == 200

    def test_drift(self):
        r = client.get("/api/v1/evaluation/drift")
        assert r.status_code == 200


# ============================================================
# Regression Tests
# ============================================================

class TestRegression:
    """Ensure Feature 4 doesn't break existing features."""

    def test_health(self):
        r = client.get("/api/v1/health")
        assert r.status_code == 200

    def test_intelligence(self):
        r = client.get("/api/v1/intelligence/summary")
        assert r.status_code == 200

    def test_crimes(self):
        r = client.get("/api/v1/crimes/?page=1&page_size=5")
        assert r.status_code == 200

    def test_patterns(self):
        r = client.get("/api/v1/patterns/stats")
        assert r.status_code == 200

    def test_trends(self):
        r = client.get("/api/v1/trends/summary")
        assert r.status_code == 200

    def test_hotspots(self):
        r = client.get("/api/v1/hotspots/stats")
        assert r.status_code == 200

    def test_maps(self):
        r = client.get("/api/v1/maps/stats")
        assert r.status_code == 200

    def test_graph(self):
        r = client.get("/api/v1/graph/stats")
        assert r.status_code == 200

    def test_timeline(self):
        r = client.get("/api/v1/criminal-timeline/stats")
        assert r.status_code == 200

    def test_behavior(self):
        r = client.get("/api/v1/behavior/stats")
        assert r.status_code == 200

    def test_mo(self):
        r = client.get("/api/v1/mo/stats")
        assert r.status_code == 200

    def test_similar_cases(self):
        r = client.get("/api/v1/similar-cases/stats")
        assert r.status_code == 200

    def test_recommendations(self):
        r = client.get("/api/v1/recommendations/dashboard")
        assert r.status_code == 200

    def test_bookmarks(self):
        r = client.get("/api/v1/bookmarks/?user_id=1")
        assert r.status_code == 200

    def test_investigations(self):
        r = client.get("/api/v1/investigations/")
        assert r.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
