from enum import Enum, unique

@unique
class GameState(Enum):
    WAITING_FOR_PLAYER = '1'
    READY = '2'
    WAITING_FOR_ACTION = '3'
    TEMINATED = '4'
    COMPLETED = '5'