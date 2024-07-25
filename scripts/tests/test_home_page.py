def test_home(client):
    response = client.get("/")
    assert response.json == {"message": "api em funcionamento"}