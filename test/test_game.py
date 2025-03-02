

from typing import Optional
from src.constants.hands import Hand
from src.models.Game import Game
from src.models.User import User
from src.constants.states import GameState

def test_create_game():
    host:User = User("Jonathan")
    game:Game = Game(host)
    assert game.users.get(host.id).name == "Jonathan"
    assert game.host == host.id


def test_join_game():
    host:User = User("Kurt")
    game:Game = Game(host)
    player:User = User("Linnea")
    game.join(player)
    print(game.users.__len__())
    print(game.users.get(host.id).name)
    print(game.users.get(player.id))
    assert game.users.get(host.id).name == "Kurt"
    assert game.users.get(player.id).name == "Linnea"


def test_play_hand():
    host:User = User('Oskar')
    game:Game = Game(host)
    assert game.get_state() == GameState.WAITING_FOR_PLAYER
    player:User = User("Patrick")
    game.join(player)
    assert game.get_state() == GameState.READY


def test_set_winner():
    host:User = User('Rolf')
    player:User = User('Steve')
    game:Game = Game(host)
    game.join(player)
    winner:Optional[str] = game.play(player.id, Hand.ROCK)
    assert winner == None
    winner = game.play(host.id, Hand.SCISSORS)
    assert winner == player.id

    winner = game.play(player.id, Hand.PAPER)
    assert winner == None
    winner = game.play(host.id, Hand.SCISSORS)
    assert winner == host.id

    winner = game.play(player.id, Hand.PAPER)
    assert winner == None
    winner = game.play(host.id, Hand.ROCK)
    assert winner == player.id

    winner = game.play(player.id, Hand.SCISSORS)
    assert winner == None
    winner = game.play(host.id, Hand.SCISSORS)
    assert winner == ''


def test_game_state():
    host:User = User('Thor')
    player:User = User('Uwe')
    game:Game = Game(host)
    assert game.get_state() == GameState.WAITING_FOR_PLAYER
    game.join(player)
    assert game.get_state() == GameState.READY
    game.play(player.id, Hand.ROCK)
    assert game.get_state() == GameState.WAITING_FOR_ACTION
    game.play(host.id, Hand.SCISSORS)
    assert game.get_state() == GameState.READY
    
