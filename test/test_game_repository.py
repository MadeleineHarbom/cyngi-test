from src.constants.hands import Hand
from src.models.player import Player
from src.models.game import Game
from src.repositories.gameRepository import GameRepository
import pytest
import uuid


@pytest.fixture
def repo():
    repo:GameRepository = GameRepository()
    yield repo
    repo.games.clear()

def test_save_game(repo:GameRepository):
    game:Game = Game(Player('Madeleine'))
    success:bool = repo.save_game(game)
    assert success == True
    assert repo.games.__len__() == 1
    another_game = Game(Player('Nina'))
    another_success:bool = repo.save_game(another_game)
    assert another_success == True
    assert repo.games.__len__() == 2


def test_get_available_games(repo:GameRepository):
    repo = GameRepository()
    host2:Player = Player('Adam')
    player1:Player = Player('Francis')
    player2:Player = Player('Gunilla')
    game1:Game = Game(Player('Bertram'))
    repo.save_game(game1)
    game2:Game = Game(host2)
    repo.save_game(game2)
    game3:Game = Game(Player('Carl'))
    repo.save_game(game3)
    game4:Game = Game(Player('Douglas'))
    repo.save_game(game4)

    assert repo.get_available_games().__len__() == 4

    game1.join(player1)
    assert repo.get_available_games().__len__() == 3
    game2.join(player2)
    game2.play(host2.id, Hand.SCISSORS)
    assert repo.get_available_games().__len__() == 2
    game2.play(player2.id, Hand.SCISSORS)
    assert repo.get_available_games().__len__() == 2



def test_get_game_by_id(repo:GameRepository):
    game:Game = Game(Player('Ingolf'))
    repo.save_game(game)
    retrieved_game:Game = repo.get_game_by_id(game.id)
    assert retrieved_game is not None
    assert retrieved_game.id == game.id


def test_get_game_by_id_exception(repo:GameRepository):
    with pytest.raises(KeyError): 
        repo.get_game_by_id(str(uuid.uuid4()))


def test_get_games(repo:GameRepository):
    game1:Game = Game(Player('Veronika'))
    repo.save_game(game1)
    game2:Game = Game(Player('Xander'))
    repo.save_game(game2)
    game3:Game = Game(Player('Yuri'))
    repo.save_game(game3)
    assert repo.get_available_games().__len__() == 3
    game3.join(Player('Zoe'))
    assert repo.get_available_games().__len__() == 2



