from typing import List
from interfaces.IGameRepository import IGameRepository

from models.Game import Game


class GameRepository(IGameRepository):
    #Make this a singleton
    def __init__(self):
        print("Game init")
        self.games:List[Game] = []

    def save_game(self, game:Game) -> bool:
        print('save game')
        try:
            self.games.append(game)
            return True
        except:
            return False
        