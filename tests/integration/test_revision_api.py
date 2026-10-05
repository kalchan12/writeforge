"""Integration tests for POST /revision/plan endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_revision_endpoint_standalone_success() -> None:
    text = (
        "The red fox ran quickly into the woods today. "
        "The old man sat quietly near the river banks. "
        "The cold wind blew sharply across the dark hills."
    )
    response = client.post("/revision/plan", json={"text": text})
    assert response.status_code == 200

    data = response.json()
    assert "goals" in data
    assert "sentence_targets" in data
    assert "total_suggestions" in data
    assert "summary" in data
    assert data["total_suggestions"] >= 1


def test_revision_endpoint_with_profile_success() -> None:
    # 1. Create a profile with concise sentences
    create_payload = {
        "author_name": "Concise Author",
        "documents": [
            {"text": "Short phrase. Brief words."},
            {"text": "Crisp statement. Tiny thought."},
        ],
    }
    create_res = client.post("/profiles/create", json=create_payload)
    assert create_res.status_code == 200
    profile_data = create_res.json()

    # 2. Plan revisions for an expansive text against this profile
    payload = {
        "text": (
            "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves. "
            "Mathematical calculations require rigorous discipline and uncompromising adherence to symbolic truth."
        ),
        "profile": profile_data,
        "outlier_threshold": 1.0,
    }
    response = client.post("/revision/plan", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["target_author"] == "Concise Author"
    assert "goals" in data
    assert "summary" in data


def test_revision_endpoint_empty_text() -> None:
    response = client.post("/revision/plan", json={"text": ""})
    assert response.status_code == 422


def test_revision_endpoint_missing_payload() -> None:
    response = client.post("/revision/plan", json={})
    assert response.status_code == 422
