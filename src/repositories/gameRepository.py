from typing import List
from src.interfaces.singleton import singleton
from src.interfaces.IGameRepository import IGameRepository

from src.models.GameList import GameList
from src.models.Game import Game

@singleton
class GameRepository(IGameRepository):
    games:List[Game] = []

    def __init__(self):
        print('Game repo init')


    def save_game(self, game:Game) -> bool:
        try:
            self.games.append(game)
            print(f"Saved game")
            print(game)
            return True
        except:
            return False
        

    def get_available_games(self) -> GameList:
        print("get available games")
        print([game for game in self.games if game.player is None])
        return GameList([game for game in self.games if game.player is None])
    
    
    def get_game_by_id(self, id:str) -> Game:
        print(f"Collecting game with id {id}")
        for game in self.games:
            if game.id == id:
                return game
        raise KeyError(f'No Game with id {id} found')
    