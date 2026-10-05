"""Integration tests for Author Profile API endpoints."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_create_profile_endpoint_success() -> None:
    payload = {
        "author_name": "Arthur Conan Doyle",
        "documents": [
            {"text": "Elementary, my dear Watson. The game is afoot."},
            {"text": "When you have eliminated the impossible, whatever remains must be the truth."},
        ],
        "metadata": {"period": "Victorian", "genre": "detective"},
    }

    response = client.post("/profiles/create", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["author_name"] == "Arthur Conan Doyle"
    assert data["document_count"] == 2
    assert data["metadata"]["period"] == "Victorian"
    assert "baselines" in data
    assert "word_count" in data["baselines"]
    assert "type_token_ratio" in data["baselines"]
    assert "yules_k" in data["baselines"]

    wc = data["baselines"]["word_count"]
    assert wc["sample_count"] == 2
    assert wc["mean"] > 0


def test_create_profile_endpoint_empty_documents_error() -> None:
    payload = {
        "author_name": "Nobody",
        "documents": [],
    }
    response = client.post("/profiles/create", json=payload)
    assert response.status_code == 422


def test_create_profile_endpoint_missing_author_error() -> None:
    payload = {
        "documents": [{"text": "Sample text."}],
    }
    response = client.post("/profiles/create", json=payload)
    assert response.status_code == 422
