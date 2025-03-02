from fastapi.testclient import TestClient
import pytest
from src.constants.states import GameState
from src.main import app
from src.models import Game
from src.repositories.gameRepository import GameRepository


client = TestClient(app)

@pytest.fixture(scope='function')
def repo_setup():
    print('test setup')
    repo:GameRepository = GameRepository()
    yield repo
    print('test taredown')
    repo.games.clear()
    print(repo.games.__len__())
    

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world!"}


def test_get_root_fail_on_wrong_message():
    response = client.get("/")
    assert response.json() != {"message": "Hello, wørld!"}


def test_host_game(repo_setup):
    request_body = {
        "name": "Ellie"
    }
    response = client.post("/host", json=request_body)

    assert response.status_code == 200
    assert "token" in response.json()
    assert "game" in response.json()
    

def test_join_game(repo_setup):
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


def test_get_games(repo_setup):
    setup_request_body_1 = {
        "name": "Camilla"
    }
    host_response_1 = client.post("/host", json=setup_request_body_1)
    setup_request_body_2 = {
        "name": "Drew"
    }
    host_response_2 = client.post("/host", json=setup_request_body_2)
    games_response_1 = client.get("/games")
 
    games_1 = games_response_1.json()
    assert games_1.__len__() == 2
    assert {"id":host_response_1.json()["game"], "name": "Camilla"} in games_1
    assert {"id":host_response_2.json()["game"], "name": "Drew"} in games_1

    game_id_1 = host_response_1.json()["game"]
    setup_request_body_3 = {
        "name": "Gert"
    }
    join_response_2 = client.post(f"/join/{game_id_1}", json=setup_request_body_3)
    games_response_2 = client.get("/games")
    print(games_response_2)
 
    games_2 = games_response_2.json()
    assert games_2.__len__() == 1
    assert {"id":host_response_1.json()["game"], "name": "Camilla"} not in games_2
    assert {"id":host_response_2.json()["game"], "name": "Drew"} in games_2



def get_state(repo_setup):
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
    