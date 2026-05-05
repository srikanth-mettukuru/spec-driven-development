def test_health_returns_200_with_ok_status(client):
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "0.1.0"
    assert response.json()["env"] == "test"

def test_ready_returns_200_with_ok_status(client):
    response = client.get("/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["version"] == "0.1.0"
    assert response.json()["env"] == "test"
