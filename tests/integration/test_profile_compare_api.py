"""Integration tests for POST /profiles/compare endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_compare_profile_endpoint_success() -> None:
    # 1. Create a profile first
    create_payload = {
        "author_name": "Test Author",
        "documents": [
            {"text": "Short simple sentence. Another clean phrase."},
            {"text": "Brief thought here. Crisp concise words."},
        ],
    }
    create_res = client.post("/profiles/create", json=create_payload)
    assert create_res.status_code == 200
    profile_data = create_res.json()

    # 2. Compare a new text against this profile
    compare_payload = {
        "profile": profile_data,
        "text": "Short clean sentence. Direct and brief.",
        "outlier_threshold": 2.5,
    }
    compare_res = client.post("/profiles/compare", json=compare_payload)
    assert compare_res.status_code == 200

    report = compare_res.json()
    assert report["author_name"] == "Test Author"
    assert "consistency_score" in report
    assert 0.0 <= report["consistency_score"] <= 1.0
    assert "deviations" in report
    assert "summary" in report


def test_compare_profile_endpoint_invalid_payload() -> None:
    response = client.post("/profiles/compare", json={})
    assert response.status_code == 422
