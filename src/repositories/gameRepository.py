from typing import List
from src.constants.states import GameState
from src.utils.singleton import singleton
from src.interfaces.igame_repository import IGameRepository

from src.models.game import Game

@singleton
class GameRepository(IGameRepository):
    games:List[Game] = [] 
    #array for simplisity and limiting scope
    #Can be exchanged for a database

    def __init__(self):
        print('Game repo init')


    def save_game(self, game:Game) -> bool:
        self.games.append(game)
        return True
  
        

    def get_available_games(self) -> List[Game]:
        return [game for game in self.games if game.state is GameState.WAITING_FOR_PLAYER.value]
    
    
    def get_game_by_id(self, id:str) -> Game:
        for game in self.games:
            if game.id == id:
                return game
        raise KeyError(f'No Game with id {id} found')
    