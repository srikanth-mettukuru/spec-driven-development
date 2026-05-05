def test_500_returns_internal_error(client):
    response = client.get("/trigger-500")
    assert response.status_code == 500
    assert response.json()["code"] == "INTERNAL_ERROR"
    assert "detail" in response.json()

def test_422_returns_validation_error(client):
    response = client.post("/trigger-validation", json={"invalid": "data"})
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
    assert "detail" in response.json()

def test_404_returns_http_error(client):
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    assert response.json()["code"] == "HTTP_ERROR"
    assert "detail" in response.json()
