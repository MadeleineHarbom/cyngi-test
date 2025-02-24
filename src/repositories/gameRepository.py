from typing import List
from src.interfaces.IGameRepository import IGameRepository

from src.models.Game import Game


class GameRepository(IGameRepository):
    #Make this a singleton
    def __init__(self):
        self.games:List[Game] = []

    def save_game(self, game:Game) -> bool:
        try:
            self.games.append(game)
            return True
        except:
            return False
        
    def get_available_games(self) -> List[Game]:
        return  [game for game in self.games if game.player is None]

        