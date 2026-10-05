"""Integration tests for persistence endpoints: GET /profiles, GET /profiles/{id}, GET /revision/logs."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_persistence_endpoints_workflow() -> None:
    # 1. Create a profile (persists to SQLite)
    create_payload = {
        "author_name": "Persistence Author",
        "documents": [
            {"text": "Short clean prose. Direct sentences here."},
            {"text": "Another crisp sentence. Clear concise text."},
        ],
    }
    create_res = client.post("/profiles/create", json=create_payload)
    assert create_res.status_code == 200
    created_profile = create_res.json()
    profile_id = created_profile["id"]

    # 2. List profiles
    list_res = client.get("/profiles")
    assert list_res.status_code == 200
    profiles = list_res.json()
    assert isinstance(profiles, list)
    assert any(p["id"] == profile_id for p in profiles)

    # 3. Get profile by ID
    get_res = client.get(f"/profiles/{profile_id}")
    assert get_res.status_code == 200
    assert get_res.json()["author_name"] == "Persistence Author"

    # 4. Get non-existent profile returns 404
    not_found_res = client.get("/profiles/non-existent-profile-id-12345")
    assert not_found_res.status_code == 404

    # 5. Execute revision (persists audit log)
    rev_payload = {
        "text": "The extraordinarily complex mechanisms manifest structural anomalies.",
        "profile": created_profile,
        "use_mock": True,
    }
    rev_res = client.post("/revision/execute", json=rev_payload)
    assert rev_res.status_code == 200

    # 6. Retrieve revision logs
    logs_res = client.get("/revision/logs")
    assert logs_res.status_code == 200
    logs = logs_res.json()
    assert isinstance(logs, list)
    assert len(logs) >= 1
    assert any(log["author_name"] == "Persistence Author" for log in logs)
