from enum import Enum

class GameState(Enum):
    WAITING_FOR_PLAYER = 1
    READY = 2
    WAITING_FOR_ACTION = 3