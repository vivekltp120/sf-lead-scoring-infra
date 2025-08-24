import pytest, json, asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_ready():
    r = client.get("/readyz")
    assert r.status_code == 200
    assert r.json()["ready"] is True

def test_score_ok():
    payload = {
        "lead_id": "L-1",
        "features": {f"f{i}": 0.5 for i in range(1, 51)}
    }
    r = client.post("/score", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert j["lead_id"] == "L-1"
    assert 1 <= j["score"] <= 5
