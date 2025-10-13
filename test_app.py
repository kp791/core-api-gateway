from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_ingest_logs_success():
    payload = {
        "source": "systemA",
        "timestamp": "2025-10-07T03:30:00Z",
        "records": [{"event": "startup"}, {"event": "shutdown"}]
    }
    headers = {"Authorization": "Bearer my-demo-token"}
    r = client.post("/logs", json=payload, headers=headers)
    assert r.status_code == 202
    data = r.json()
    assert data["accepted"] is True
    assert data["source"] == "systemA"
    assert data["count"] == 2

def test_ingest_logs_unauthorized():
    payload = {
        "source": "systemA",
        "timestamp": "2025-10-07T03:30:00Z",
        "records": [{"event": "startup"}]
    }
    headers = {"Authorization": "Bearer wrong-token"}
    r = client.post("/logs", json=payload, headers=headers)
    assert r.status_code == 401
    assert r.json()["detail"] == "Unauthorized"

def test_ingest_logs_invalid():
    payload = {
        "source": "systemA",
        "records": [{"event": "startup"}]  # missing timestamp
    }
    headers = {"Authorization": "Bearer my-demo-token"}
    r = client.post("/logs", json=payload, headers=headers)
    assert r.status_code == 422  # Pydantic validation
