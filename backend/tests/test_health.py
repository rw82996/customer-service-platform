def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["version"] == "2.0.0"


def test_security_headers(client):
    resp = client.get("/api/health")
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"
    assert resp.headers.get("X-Frame-Options") == "DENY"
    assert "max-age" in resp.headers.get("Strict-Transport-Security", "")
    assert resp.headers.get("X-Correlation-ID") is not None
