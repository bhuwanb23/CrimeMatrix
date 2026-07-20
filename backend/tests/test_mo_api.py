import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_mo_stats():
    response = client.get("/api/v1/mo/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "total_profiles" in data["data"]


def test_list_profiles():
    response = client.get("/api/v1/mo/profiles")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "items" in data["data"]


def test_fingerprint_crime():
    response = client.post("/api/v1/mo/fingerprint/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_batch_fingerprint():
    response = client.post("/api/v1/mo/batch-fingerprint")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "crimes_processed" in data["data"]


def test_compare_profiles():
    # First create two profiles
    client.post("/api/v1/mo/fingerprint/1")

    # Get profiles
    response = client.get("/api/v1/mo/profiles")
    profiles = response.json().get("data", {}).get("items", [])

    if len(profiles) >= 1:
        # Compare with itself
        response = client.post("/api/v1/mo/compare", json={
            "profile_id_1": profiles[0]["id"],
            "profile_id_2": profiles[0]["id"]
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "similarity_score" in data["data"]


def test_find_similar():
    # Create a profile first
    client.post("/api/v1/mo/fingerprint/1")

    response = client.get("/api/v1/mo/profiles")
    profiles = response.json().get("data", {}).get("items", [])

    if profiles:
        response = client.get(f"/api/v1/mo/similar/{profiles[0]['id']}?top_k=3")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


def test_regression_intelligence():
    response = client.get("/api/v1/intelligence/summary")
    assert response.status_code == 200


def test_regression_hotspots():
    response = client.get("/api/v1/hotspots/stats")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
