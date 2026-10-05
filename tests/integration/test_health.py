"""Integration test for the FastAPI health check endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """GET /health must return 200 with structured status information."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "rightforge-api"
    assert data["version"] == "0.1.0"
