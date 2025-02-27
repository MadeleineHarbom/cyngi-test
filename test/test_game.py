

from src.models.Game import Game
from src.models.User import User

def test_create_game():
    host:User = User("Jonathan")
    game:Game = Game(host)
    assert game.users.get(host.id).name == "Jonathan"
    assert game.host == host.id

'''
def test_join_game():
    host:User = User("Kurt", host=True)
    game:Game = Game(host)
    player:User = User("Linnea")
    game.join(player)

    assert game.users.get(host.id).name == "Kurt"
    assert game.users.get(player.id).name == "Linnea"
    '''
