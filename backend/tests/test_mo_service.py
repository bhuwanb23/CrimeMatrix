import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.mo_service import MOService


class MockDB:
    def __init__(self):
        self._data = {}
        self._committed = False

    async def execute(self, stmt):
        return MockResult([])

    async def commit(self):
        self._committed = True

    async def flush(self):
        pass

    def add(self, obj):
        pass


class MockResult:
    def __init__(self, scalars):
        self._scalars = scalars

    def scalars(self):
        return MockScalarResult(self._scalars)

    def scalar(self):
        return self._scalars[0] if self._scalars else None


class MockScalarResult:
    def __init__(self, data):
        self._data = data

    def all(self):
        return self._data

    def first(self):
        return self._data[0] if self._data else None


# Unit tests for MO feature extraction
def test_extract_features_burglary():
    db = MockDB()
    svc = MOService(db)
    text = "Broke window at night, used knife to threaten victim, stole jewelry and cash"
    features = svc._extract_features(text)

    assert "window" in features["entry"]
    assert "night" in features["time"]
    assert "knife" in features["weapon"]
    assert "jewelry" in features["target"]
    assert "cash" in features["target"]


def test_extract_features_theft():
    db = MockDB()
    svc = MOService(db)
    text = "grabbed phone from victim's hand and snatched wallet, then escaped on bike"
    features = svc._extract_features(text)

    assert "grab" in features["method"]
    assert "snatch" in features["method"]
    assert "phone" in features["target"]
    assert "wallet" in features["target"]
    assert "bike" in features["transport"]


def test_extract_features_empty():
    db = MockDB()
    svc = MOService(db)
    features = svc._extract_features("")

    for key in features:
        assert features[key] == ""


def test_build_mo_text():
    db = MockDB()
    svc = MOService(db)
    features = {"entry": "window, door", "weapon": "knife", "target": "jewelry", "time": "", "method": "", "transport": "", "exit": "", "location": ""}
    text = svc._build_mo_text(features)

    assert "entry: window, door" in text
    assert "weapon: knife" in text
    assert "target: jewelry" in text
    assert "time:" not in text


def test_create_embedding():
    db = MockDB()
    svc = MOService(db)
    features = {"entry": "window", "weapon": "knife", "target": "jewelry", "time": "", "method": "", "transport": "", "exit": "", "location": ""}
    embedding = svc._create_embedding(features)

    assert isinstance(embedding, list)
    assert len(embedding) > 0
    # Should have 1s for matching keywords
    assert 1.0 in embedding


def test_profile_to_dict():
    db = MockDB()
    svc = MOService(db)

    class MockProfile:
        id = 1
        crime_id = 10
        case_id = None
        entry_method = "window"
        exit_method = ""
        timing_pattern = "night"
        weapon_type = "knife"
        target_type = "jewelry"
        location_pattern = ""
        victim_profile = ""
        escape_method = "bike"
        mo_text = "entry: window; time: night; weapon: knife"
        fingerprint_json = json.dumps({"entry": "window", "weapon": "knife"})
        confidence = 75.0

    result = svc._profile_to_dict(MockProfile())

    assert result["id"] == 1
    assert result["crime_id"] == 10
    assert result["entry_method"] == "window"
    assert result["confidence"] == 75.0
    assert result["fingerprint"]["entry"] == "window"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
