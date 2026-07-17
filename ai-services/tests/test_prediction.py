import pytest
from prediction.crime_forecast import CrimeForecasting
from prediction.hotspot import HotspotPrediction
from prediction.repeat_offender import RepeatOffenderPrediction
from prediction.risk_scoring import RiskScoring
from prediction.mo_similarity import MOSimilarity
from prediction.case_recommender import CaseRecommendation
from prediction.engine import PredictionEngine


class TestCrimeForecasting:
    def setup_method(self):
        self.fc = CrimeForecasting()

    def test_forecast_basic(self):
        data = [{"period": "2024-01", "count": 10}, {"period": "2024-02", "count": 15}, {"period": "2024-03", "count": 20}]
        result = self.fc.forecast(data)
        assert result["trend"] == "increasing"
        assert len(result["predictions"]) == 1
        assert result["predictions"][0]["count"] >= 15

    def test_forecast_empty(self):
        result = self.fc.forecast([])
        assert result["trend"] == "insufficient_data"

    def test_forecast_single(self):
        result = self.fc.forecast([{"period": "2024-01", "count": 10}])
        assert result["predictions"][0]["count"] == 10

    def test_detect_anomalies(self):
        data = [{"period": "m1", "count": 10}, {"period": "m2", "count": 11}, {"period": "m3", "count": 50}]
        anomalies = self.fc.detect_anomalies(data)
        assert len(anomalies) >= 1
        assert anomalies[0]["type"] == "spike"


class TestHotspotPrediction:
    def setup_method(self):
        self.hp = HotspotPrediction()

    def test_identify_hotspots(self):
        crimes = [
            {"district": "Bangalore", "crime_type": "theft"},
            {"district": "Bangalore", "crime_type": "theft"},
            {"district": "Bangalore", "crime_type": "robbery"},
            {"district": "Mysore", "crime_type": "theft"},
        ]
        hotspots = self.hp.identify_hotspots(crimes)
        assert len(hotspots) > 0
        assert hotspots[0]["location"] == "Bangalore"

    def test_hotspot_risk_levels(self):
        crimes = [{"district": "A", "crime_type": "theft"} for _ in range(25)]
        hotspots = self.hp.identify_hotspots(crimes)
        assert hotspots[0]["risk_level"] == "critical"

    def test_hotspot_trend(self):
        crimes = [
            {"district": "X", "created_at": "2024-01", "crime_type": "theft"},
            {"district": "X", "created_at": "2024-02", "crime_type": "theft"},
        ]
        trend = self.hp.hotspot_trend("X", crimes)
        assert "trend" in trend


class TestRepeatOffenderPrediction:
    def setup_method(self):
        self.ro = RepeatOffenderPrediction()

    def test_high_risk(self):
        profile = {"prior_offenses": 7, "age": 25, "risk_score": 0.8, "years_since_last_offense": 0.5}
        result = self.ro.predict(profile)
        assert result["risk_level"] in ("high", "very_high")
        assert result["risk_score"] > 50

    def test_low_risk(self):
        profile = {"prior_offenses": 0, "age": 50, "risk_score": 0.1, "years_since_last_offense": 10}
        result = self.ro.predict(profile)
        assert result["risk_level"] == "low"

    def test_batch_predict(self):
        profiles = [{"prior_offenses": 5}, {"prior_offenses": 0}]
        results = self.ro.batch_predict(profiles)
        assert len(results) == 2


class TestRiskScoring:
    def setup_method(self):
        self.rs = RiskScoring()

    def test_high_risk(self):
        profile = {"prior_offenses": 8, "offense_severity": "severe", "age": 22, "district": "X", "high_risk_areas": ["X"], "associates_with_criminal_record": 4, "years_since_last_offense": 0.5}
        result = self.rs.score(profile)
        assert result["risk_score"] > 50
        assert result["risk_level"] in ("high", "very_high")

    def test_low_risk(self):
        profile = {"prior_offenses": 0, "offense_severity": "minor", "age": 45, "district": "Y", "high_risk_areas": ["X"], "associates_with_criminal_record": 0, "years_since_last_offense": 10}
        result = self.rs.score(profile)
        assert result["risk_score"] < 30

    def test_compare(self):
        profiles = [{"prior_offenses": 8}, {"prior_offenses": 1}]
        compared = self.rs.compare(profiles)
        assert compared[0]["risk_score"] >= compared[1]["risk_score"]


class TestMOSimilarity:
    def setup_method(self):
        self.mo = MOSimilarity()

    def test_identical_mo(self):
        result = self.mo.compare("broke window at night stole jewelry", "broke window at night stole jewelry")
        assert result["similarity_score"] > 80

    def test_similar_mo(self):
        result = self.mo.compare("broke door at night stole cash", "forced window at night grabbed jewelry")
        assert result["similarity_score"] > 30

    def test_different_mo(self):
        result = self.mo.compare("con victim into giving money", "broke into house at night")
        assert result["similarity_score"] < 50

    def test_find_similar(self):
        mos = [
            {"case_id": 1, "description": "broke window at night stole jewelry"},
            {"case_id": 2, "description": "con artist tricked victim"},
        ]
        results = self.mo.find_similar_mos("broke door at night", mos)
        assert results[0]["case_id"] == 1


class TestCaseRecommendation:
    def setup_method(self):
        self.cr = CaseRecommendation()

    def test_recommend(self):
        target = {"id": 1, "crime_type": "theft", "district": "Bangalore", "description": "stole jewelry from shop"}
        cases = [
            {"id": 2, "crime_type": "theft", "district": "Bangalore", "description": "stole jewelry from store"},
            {"id": 3, "crime_type": "murder", "district": "Mysore", "description": "violent crime"},
        ]
        recs = self.cr.recommend(target, cases)
        assert len(recs) > 0
        assert recs[0]["case_id"] == 2

    def test_no_self_recommendation(self):
        target = {"id": 1, "crime_type": "theft"}
        cases = [{"id": 1, "crime_type": "theft"}]
        recs = self.cr.recommend(target, cases)
        assert len(recs) == 0


class TestPredictionEngine:
    def setup_method(self):
        self.engine = PredictionEngine()

    @pytest.mark.asyncio
    async def test_forecast(self):
        result = await self.engine.predict("forecast", {"historical": [{"period": "m1", "count": 10}, {"period": "m2", "count": 15}]})
        assert "predictions" in result

    @pytest.mark.asyncio
    async def test_risk(self):
        result = await self.engine.predict("risk", {"profile": {"prior_offenses": 5}})
        assert "risk_score" in result

    @pytest.mark.asyncio
    async def test_unknown(self):
        result = await self.engine.predict("unknown", {})
        assert "error" in result

    def test_stats(self):
        stats = self.engine.get_stats()
        assert "prediction_types" in stats
