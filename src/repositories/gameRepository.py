from typing import List
from src.constants.states import GameState
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
        return GameList([game for game in self.games if game.state is GameState.WAITING_FOR_PLAYER])
    
    
    def get_game_by_id(self, id:str) -> Game:
        for game in self.games:
            if game.id == id:
                return game
        raise KeyError(f'No Game with id {id} found')
    