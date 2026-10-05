"""Integration tests for POST /analysis/linguistic endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_linguistic_analysis_endpoint_success() -> None:
    response = client.post(
        "/analysis/linguistic",
        json={"text": "Short sentence. Another sentence with unique vocabulary!"},
    )
    assert response.status_code == 200

    data = response.json()
    assert "document_id" in data
    assert "metrics" in data

    metrics = data["metrics"]
    assert "type_token_ratio" in metrics
    assert "sentence_length_mean" in metrics
    assert "punct_exclamation_count" in metrics
    assert metrics["punct_exclamation_count"]["value"] == 1


def test_linguistic_analysis_endpoint_empty_text() -> None:
    response = client.post(
        "/analysis/linguistic",
        json={"text": ""},
    )
    assert response.status_code == 200
    data = response.json()
    metrics = data["metrics"]
    assert metrics["total_word_count"]["value"] == 0
    assert metrics["type_token_ratio"]["value"] == 0.0


def test_linguistic_analysis_endpoint_missing_payload() -> None:
    response = client.post("/analysis/linguistic", json={})
    assert response.status_code == 422
