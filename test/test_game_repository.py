from typing import List
from src.constants.hands import Hand
from src.models.User import User
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
    game:Game = Game(User("Madeleine"))
    success:bool = repo.save_game(game)
    assert success == True
    assert repo.games.__len__() == 1
    another_game = Game(User("Nina"))
    another_success:bool = repo.save_game(another_game)
    assert another_success == True
    assert repo.games.__len__() == 2


def test_get_available_games(repo:GameRepository):
    repo = GameRepository()
    game1:Game = Game(User("Adam"))
    repo.save_game(game1)
    game2:Game = Game(User("Bertram"))
    repo.save_game(game2)
    game3:Game = Game(User("Carl"))
    repo.save_game(game3)
    game4:Game = Game(User("Douglas"))
    repo.save_game(game4)

    games:List[Game] = repo.get_available_games()
    assert games.__len__() == 4

    game4.join(User("Francis"))
    available_games:List[Game] = repo.get_available_games()

    assert available_games.__len__() == 3


def test_get_game_by_id(repo:GameRepository):
    game:Game = Game(User('Ingolf'))
    repo.save_game(game)
    retrieved_game:Game = repo.get_game_by_id(game.id)
    assert retrieved_game is not None
    assert retrieved_game.id == game.id


def test_get_game_by_id_exception(repo:GameRepository):
    with pytest.raises(KeyError): 
        repo.get_game_by_id(str(uuid.uuid4()))


def test_get_games(repo:GameRepository):
    game1:Game = Game(User("Veronika"))
    repo.save_game(game1)
    game2:Game = Game(User("Xander"))
    repo.save_game(game2)
    game3:Game = Game(User("Yuri"))
    repo.save_game(game3)
    assert repo.get_available_games().__len__() == 3
    game3.join(User('Zoe'))
    assert repo.get_available_games().__len__() == 2

def test_get_only_joinable_games(repo:GameRepository):
    host:User = User('Andrea')
    player:User = User('Bertine')
    game:Game = Game(host)
    repo.save_game(game)
    assert repo.get_available_games().__len__() == 1
    game.join(player)
    assert repo.get_available_games().__len__() == 0
    game.play(host.id, Hand.SCISSORS)
    assert repo.get_available_games().__len__() == 0
    game.play(player.id, Hand.SCISSORS)
    assert repo.get_available_games().__len__() == 0

