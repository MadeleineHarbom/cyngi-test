

from typing import Optional

import pytest
from src.constants.hands import Hand
from src.models.Game import Game
from src.models.Player import Player
from src.constants.states import GameState

def test_create_game():
    host:Player = Player("Jonathan")
    game:Game = Game(host)
    assert game.users.get(host.id).name == "Jonathan"
    assert game.host == host.id


def test_join_game():
    host:Player = Player("Kurt")
    game:Game = Game(host)
    player:Player = Player("Linnea")
    game.join(player)
    assert game.users.get(host.id).name == "Kurt"
    assert game.users.get(player.id).name == "Linnea"


def test_play_hand():
    host:Player = Player('Oskar')
    game:Game = Game(host)
    assert game.get_state() == GameState.WAITING_FOR_PLAYER
    player:Player = Player("Patrick")
    game.join(player)
    assert game.get_state() == GameState.READY


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
    assert game.get_state() == GameState.WAITING_FOR_PLAYER
    game.join(player)
    assert game.get_state() == GameState.READY
    game.play(player.id, Hand.ROCK)
    assert game.get_state() == GameState.WAITING_FOR_ACTION
    game.play(host.id, Hand.SCISSORS)
    assert game.get_state() == GameState.READY

def test_double_turn_error():
    host:Player = Player('Clause')
    player:Player = Player('Dominico')
    game:Game = Game(host)
    game.join(player)
    game.play(host.id, Hand.SCISSORS)
    with pytest.raises(PermissionError): 
        game.play(host, Hand.PAPER)
    
