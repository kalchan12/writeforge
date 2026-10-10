"""Integration tests for POST /analysis/ai-detect endpoint."""

from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)


def test_ai_detect_endpoint_success():
    ai_text = (
        "In the ever-evolving landscape of artificial intelligence, it is paramount to delve into the rich tapestry "
        "of technology. Furthermore, this serves as a testament to human innovation, which plays a pivotal role. "
        "Moreover, we must foster collaborative solutions to seamlessly leverage these capabilities."
    )
    response = client.post("/analysis/ai-detect", json={"text": ai_text})
    assert response.status_code == 200

    data = response.json()
    assert "ai_score" in data
    assert "ai_score_percent" in data
    assert "verdict" in data
    assert "confidence" in data
    assert "signals" in data
    assert "summary" in data
    assert data["ai_score_percent"] > 50.0
    assert len(data["signals"]) > 0


def test_ai_detect_endpoint_empty_text():
    response = client.post("/analysis/ai-detect", json={"text": ""})
    assert response.status_code == 200

    data = response.json()
    assert data["ai_score"] == 0.0
    assert data["ai_score_percent"] == 0.0
    assert data["verdict"] == "No Content"
    assert data["signals"] == []
