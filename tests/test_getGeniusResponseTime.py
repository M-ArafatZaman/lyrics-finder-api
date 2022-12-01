"""
Test the /lyrics-finder-api/get-genius-response-time/
"""

def test_getGeniusResponseTime(client):
    response = client.get("/lyrics-finder-api/get-genius-response-time/")

    assert response.status_code == 200
    assert response.json.get("time") != None