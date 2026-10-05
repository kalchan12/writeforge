"""Integration tests for POST /analysis/coherence endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_coherence_endpoint_success() -> None:
    text = (
        "Linguistic research explores structural syntax and lexical diversity.\n\n"
        "These lexical structures reveal authorial invariants across diverse writing samples."
    )
    response = client.post("/analysis/coherence", json={"text": text})
    assert response.status_code == 200

    data = response.json()
    assert data["paragraph_count"] == 2
    assert "mean_paragraph_coherence" in data
    assert "paragraph_transitions" in data
    assert len(data["paragraph_transitions"]) == 1
    assert data["paragraph_transitions"][0]["jaccard_similarity"] > 0
    assert "summary" in data


def test_coherence_endpoint_empty_text() -> None:
    response = client.post("/analysis/coherence", json={"text": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["paragraph_count"] == 0
    assert data["mean_paragraph_coherence"] == 0.0


def test_coherence_endpoint_missing_payload() -> None:
    response = client.post("/analysis/coherence", json={})
    assert response.status_code == 422
