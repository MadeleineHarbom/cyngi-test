

from src.models.Game import Game


def test_create_game():
    game:Game = Game("Madeleine")
    assert game.host.name == "Madeleine"


def test_join_game():
    game:Game = Game("Player1")
    game.join("Player2")

    assert game.host.name == "Player1"
    assert game.player.name == "Player2"
