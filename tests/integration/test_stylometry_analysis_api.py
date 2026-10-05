"""Integration tests for POST /analysis/stylometry endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_stylometry_endpoint_success() -> None:
    response = client.post(
        "/analysis/stylometry",
        json={"text": "The author wrote an elegant novel with remarkable prose."},
    )
    assert response.status_code == 200

    data = response.json()
    assert "document_id" in data
    assert "metrics" in data

    metrics = data["metrics"]
    assert "yules_k" in metrics
    assert "hapax_legomena_count" in metrics
    assert "function_word_ratio" in metrics
    assert "flesch_reading_ease" in metrics
    assert "flesch_kincaid_grade" in metrics


def test_stylometry_endpoint_empty_text() -> None:
    response = client.post(
        "/analysis/stylometry",
        json={"text": ""},
    )
    assert response.status_code == 200
    data = response.json()
    metrics = data["metrics"]
    assert metrics["yules_k"]["value"] == 0.0
    assert metrics["function_word_count"]["value"] == 0


def test_stylometry_endpoint_missing_payload() -> None:
    response = client.post("/analysis/stylometry", json={})
    assert response.status_code == 422
