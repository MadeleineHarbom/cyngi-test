from abc import ABC, abstractmethod

from models import Game


class IGameRepository(ABC):

    @abstractmethod
    def save_game(self, game:Game) -> bool:
        raise NotImplementedError
        
    