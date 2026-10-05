"""Integration tests for POST /analysis/basic endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_basic_analysis_endpoint_success() -> None:
    response = client.post(
        "/analysis/basic",
        json={"text": "First sentence. Second sentence with words."},
    )
    assert response.status_code == 200

    data = response.json()
    assert "document_id" in data
    assert data["document_id"] is not None
    assert "metrics" in data

    metrics = data["metrics"]
    assert metrics["sentence_count"]["value"] == 2
    assert metrics["word_count"]["value"] == 6
    assert metrics["paragraph_count"]["value"] == 1
    assert metrics["avg_words_per_sentence"]["value"] == 3.0


def test_basic_analysis_endpoint_empty_text() -> None:
    response = client.post(
        "/analysis/basic",
        json={"text": ""},
    )
    assert response.status_code == 200
    data = response.json()
    metrics = data["metrics"]
    assert metrics["word_count"]["value"] == 0
    assert metrics["sentence_count"]["value"] == 0


def test_basic_analysis_endpoint_with_metadata() -> None:
    response = client.post(
        "/analysis/basic",
        json={
            "text": "Hello world.",
            "metadata": {"source": "unit-test", "language": "en"},
        },
    )
    assert response.status_code == 200
    data = response.json()
    metrics = data["metrics"]
    assert metrics["word_count"]["value"] == 2


def test_basic_analysis_endpoint_missing_payload() -> None:
    response = client.post("/analysis/basic", json={})
    assert response.status_code == 422
