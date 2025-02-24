from fastapi.testclient import TestClient
from src.main import app
from src.models import Game


client = TestClient(app)  # Create a test client

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}

def test_get_root_fail_on_wrong_message():
    response = client.get("/")
    assert response.json() != {"message": "Hello, wørld!"}

def test_host_game():
    request_body = {
        "name": "Eric"
    }
    response = client.post("/host", json=request_body)

    assert response.status_code == 200
    assert "token" in response.json()
    assert "game" in response.json()
    

def test_join_game():
    setup_request_body = {
        "name": "Henry"
    }
    response = client.post("/host", json=request_body)
    game_id:str = response.json()["game"]
    request_body = {
        "name": "Gunhilde"
    }
    response = client.post(f"/join/{game_id}")
    assert response.status_code == 200
 
