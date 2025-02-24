

from typing import List
from src.models.Game import Game
from src.repositories.gameRepository import GameRepository
import pytest


@pytest.fixture
def game_repo():
    repo = GameRepository()
    yield repo
    repo.games.clear()


def test_save_game(game_repo):
    game:Game = Game("Madeleine")
    success:bool = game_repo.save_game(game)
    assert success == True
    assert game_repo.games.__len__() == 1
    another_game = Game("Made")
    another_success:bool = game_repo.save_game(another_game)
    assert another_success == True
    assert game_repo.games.__len__() == 2


def test_get_available_games(game_repo):
    game1:Game = Game("Adam")
    game_repo.save_game(game1)
    game2:Game = Game("Bertram")
    game_repo.save_game(game2)
    game3:Game = Game("Carl")
    game_repo.save_game(game3)
    game4:Game = Game("Douglas")
    game_repo.save_game(game4)

    games:List[Game] = game_repo.get_available_games()
    assert games.__len__() == 4

    game4.join("Francis")
    available_games:List[Game] = game_repo.get_available_games()

    assert available_games.__len__() == 3






    

