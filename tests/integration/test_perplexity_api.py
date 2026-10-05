"""Integration tests for POST /analysis/perplexity endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_perplexity_endpoint_success() -> None:
    text = (
        "The quick brown fox jumps over the lazy dog. "
        "Every word chosen by a careful author carries acoustic texture."
    )
    response = client.post("/analysis/perplexity", json={"text": text})
    assert response.status_code == 200

    data = response.json()
    assert data["sentence_count"] == 2
    assert "overall_perplexity" in data
    assert data["overall_perplexity"] > 0
    assert "burstiness" in data
    assert "sentence_perplexities" in data
    assert len(data["sentence_perplexities"]) == 2
    assert "summary" in data


def test_perplexity_endpoint_empty_text() -> None:
    response = client.post("/analysis/perplexity", json={"text": ""})
    assert response.status_code == 200

    data = response.json()
    assert data["sentence_count"] == 0
    assert data["overall_perplexity"] == 0.0
    assert data["burstiness"] == 0.0
    assert data["sentence_perplexities"] == []


def test_perplexity_endpoint_missing_payload() -> None:
    response = client.post("/analysis/perplexity", json={})
    assert response.status_code == 422
