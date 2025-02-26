from abc import ABC, abstractmethod
from typing import List

from src.models.Game import Game


class IGameRepository(ABC):
    @abstractmethod
    def save_game(self, game:Game) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def get_available_games() -> List[Game]:
        raise NotImplementedError
    
    @abstractmethod
    def get_game_by_id() -> Game:
        raise NotImplementedError
        
    