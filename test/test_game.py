

from src.models.Game import Game


def test_create_game():
    game:Game = Game("Madeleine")
    assert game.host.name == "Madeleine"

