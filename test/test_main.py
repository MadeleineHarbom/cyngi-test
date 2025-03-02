from fastapi.testclient import TestClient
import pytest
from src.constants.states import GameState
from src.main import app
from src.models import Game
from src.repositories.gameRepository import GameRepository


client = TestClient(app)

@pytest.fixture
def repo():
    repo:GameRepository = GameRepository()
    yield repo
    repo.games.clear()

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
    response = client.post("/host", json=setup_request_body)
    game_id:str = response.json()["game"]
    request_body = {
        "name": "Gunhilde"
    }
    response = client.post(f"/join/{game_id}", json=request_body)
    assert response.status_code == 200

def test_get_games():
    #TODO ock the repo
    pass

def get_state():
    request_body = {
        "name": "Eric"
    }
    response = client.post("/host", json=request_body)
    game_id:str = response.json()["game"]
    response = client.get(f"/state/{game_id}")
    assert response.json()["State"] == GameState.WAITING_FOR_PLAYER
    request_body = {
        "name": "Frederike"
    }
    response = client.post(f"/join/{game_id}", json=request_body)
    response = client.get(f"/state/{game_id}")
    assert response.json()["State"] == GameState.READY