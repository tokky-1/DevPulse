
def test_health_check(client):
    response = client.get("/health")       # make a GET request to "/health"
    assert response.status_code == 200          # check status code
    assert response.json()["status"] == "ok"  # check the value