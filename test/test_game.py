from typing import Optional

import pytest
from transitions import MachineError
from src.constants.hands import Hand
from src.models.game import Game
from src.models.player import Player
from src.constants.states import GameState

def test_create_game():
    host:Player = Player('Jonathan')
    game:Game = Game(host)
    assert game.users.get(host.id).name == 'Jonathan'
    assert game.host == host.id


def test_join_game():
    host:Player = Player('Kurt')
    game:Game = Game(host)
    player:Player = Player('Linnea')
    game.join(player)
    assert game.users.get(host.id).name == 'Kurt'
    assert game.users.get(player.id).name == 'Linnea'


def test_play_hand():
    host:Player = Player('Oskar')
    game:Game = Game(host)
    assert game.state == GameState.WAITING_FOR_PLAYER.value
    player:Player = Player('Patrick')
    game.join(player)
    assert game.state == GameState.READY.value


def test_set_winner():
    host:Player = Player('Rolf')
    player:Player = Player('Steve')
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
    host:Player = Player('Thor')
    player:Player = Player('Uwe')
    game:Game = Game(host)
    assert game.state == GameState.WAITING_FOR_PLAYER.value
    game.join(player)
    assert game.state == GameState.READY.value
    game.play(player.id, Hand.ROCK)
    assert game.state == GameState.WAITING_FOR_ACTION.value
    game.play(host.id, Hand.SCISSORS)
    assert game.state == GameState.READY.value


def test_double_turn_error():
    host:Player = Player('Claude')
    player:Player = Player('Dominico')
    game:Game = Game(host)
    game.join(player)
    game.play(host.id, Hand.SCISSORS)
    with pytest.raises(PermissionError): 
        game.play(host, Hand.PAPER)


def test_leave_game():
    host1:Player = Player('Linda')
    game1:Game = Game(host1)
    left1: bool = game1.leave(host1.id)
    assert left1 == True

    host2:Player = Player('Morten')
    game2:Game = Game(host2)
    player2:Player = Player('Nora')
    game2.join(player2)
    left2:bool = game2.leave(player2.id)
    assert left2 == True

    host3:Player = Player('Oswald')
    game3:Game = Game(host3)
    player3:Player = Player('Petri')
    game3.join(player3)
    game3.play(host3.id, Hand.SCISSORS)
    game3.play(player3.id, Hand.ROCK)
    left3:bool = game3.leave(player3.id)
    assert left3 == True

    host4:Player = Player('Roland')
    game4:Game = Game(host4)
    player4:Player = Player('Tim')
    game4.join(player4)
    game4.play(host4.id, Hand.SCISSORS)
    with pytest.raises(MachineError):
        game4.leave(player4.id)


