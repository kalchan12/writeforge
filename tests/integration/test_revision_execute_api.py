"""Integration tests for POST /revision/execute endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_revision_execute_endpoint_mock_success() -> None:
    payload = {
        "text": (
            "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves. "
            "Mathematical calculations require rigorous discipline and uncompromising adherence to symbolic truth."
        ),
        "use_mock": True,
    }
    response = client.post("/revision/execute", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "original_text" in data
    assert "revised_text" in data
    assert len(data["revised_text"]) > 0
    assert "plan" in data
    assert "metrics_before" in data
    assert "metrics_after" in data


def test_revision_execute_endpoint_with_profile_success() -> None:
    # 1. Create reference profile
    create_payload = {
        "author_name": "Test Author",
        "documents": [
            {"text": "Short clean prose. Direct sentences here."},
            {"text": "Another crisp sentence. Clear concise text."},
        ],
    }
    create_res = client.post("/profiles/create", json=create_payload)
    assert create_res.status_code == 200
    profile_data = create_res.json()

    # 2. Execute revision with profile guidance
    payload = {
        "text": (
            "The extraordinarily intricate computational mechanisms manifest significant structural anomalies "
            "across all empirical observation intervals."
        ),
        "profile": profile_data,
        "use_mock": True,
        "outlier_threshold": 1.5,
    }
    response = client.post("/revision/execute", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["consistency_before"] is not None
    assert data["consistency_after"] is not None


def test_revision_execute_endpoint_empty_text() -> None:
    response = client.post("/revision/execute", json={"text": "", "use_mock": True})
    assert response.status_code == 422


def test_revision_execute_endpoint_missing_payload() -> None:
    response = client.post("/revision/execute", json={})
    assert response.status_code == 422
