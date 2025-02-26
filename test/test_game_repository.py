from typing import List
from src.models import GameList
from src.models.Game import Game
from src.repositories.gameRepository import GameRepository
import pytest
import uuid


@pytest.fixture
def repo():
    repo:GameRepository = GameRepository()
    yield repo
    repo.games.clear()

def test_save_game(repo:GameRepository):
    game:Game = Game("Madeleine")
    success:bool = repo.save_game(game)
    assert success == True
    assert repo.games.__len__() == 1
    another_game = Game("Made")
    another_success:bool = repo.save_game(another_game)
    assert another_success == True
    assert repo.games.__len__() == 2


def test_get_available_games(repo:GameRepository):
    repo = GameRepository()
    game1:Game = Game("Adam")
    repo.save_game(game1)
    game2:Game = Game("Bertram")
    repo.save_game(game2)
    game3:Game = Game("Carl")
    repo.save_game(game3)
    game4:Game = Game("Douglas")
    repo.save_game(game4)

    games:GameList = repo.get_available_games()
    assert games.__len__() == 4

    game4.join("Francis")
    available_games:GameList = repo.get_available_games()

    assert available_games.__len__() == 3


def test_get_game_by_id(repo:GameRepository):
    game:Game = Game('Ingolf')
    repo.save_game(game)
    retrieved_game:Game = repo.get_game_by_id(game.id)
    assert retrieved_game is not None
    assert retrieved_game.id == game.id


def test_get_game_by_id_exception(repo:GameRepository):
    with pytest.raises(KeyError): 
        repo.get_game_by_id(str(uuid.uuid4()))

