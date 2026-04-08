from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_translate_empty():
    """Test translation with empty text."""
    response = client.post("/api/translate", json={"text": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["original"] == ""
    assert data["translated"] == ""


def test_translate_whitespace():
    """Test translation with whitespace-only text."""
    response = client.post("/api/translate", json={"text": "   "})
    assert response.status_code == 200
    data = response.json()
    assert data["original"] == ""
    assert data["translated"] == ""
