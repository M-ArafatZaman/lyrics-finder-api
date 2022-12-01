
"""
Test /ping/ route
"""

def test_ping(client):
    response = client.get("/ping/")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json.get("status") == "OK"