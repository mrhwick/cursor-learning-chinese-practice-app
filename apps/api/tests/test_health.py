from fastapi.testclient import TestClient


def test_health_ok(client: TestClient) -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"ok": True}

