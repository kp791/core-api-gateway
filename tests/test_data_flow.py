from app.schemas import CleanedRecord

def test_ingest_success(client):
    payload = {
        "source_type": "csv",
        "records": [{"id": 1, "value": "ok"}],
        "batch_id": "batch001"
    }
    res = client.post("/ingest", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "accepted"
    assert data["records"] == 1


def test_ingest_duplicate_batch(client):
    payload = {"source_type": "json", "records": [{}], "batch_id": "batch001"}
    res = client.post("/ingest", json=payload)
    assert res.status_code == 400
    assert res.json()["error_code"] == "BATCH_DUPLICATE"


def test_clean_batch(client):
    res = client.post("/clean", params={"batch_id": "batch001"})
    data = res.json()
    assert res.status_code == 200
    assert len(data["cleaned"]) == 1
    parsed = CleanedRecord(**data["cleaned"][0])
    assert parsed.is_valid is True


def test_missing_batch(client):
    res = client.post("/clean", params={"batch_id": "badbatch"})
    assert res.status_code == 404
    assert res.json()["error_code"] == "BATCH_NOT_FOUND"


def test_summarize_records(client):
    cleaned = [{"record_id": "batch001-0", "normalized": {"id": 1}, "is_valid": True}]
    body = {"batch_id": "batch001", "clean_records": cleaned, "ai_mode": "ops"}
    res = client.post("/summarize", json=body)
    data = res.json()
    assert res.status_code == 200
    assert "operational insights" in data["summary"]

