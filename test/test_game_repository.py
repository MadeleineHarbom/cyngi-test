

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

    

