from typing import Dict, Optional
import uuid
from src.constants.states import GameState
from src.constants.hands import Hand
from src.models.User import User

class Game:
    def __init__(self, host:User):
        self.users:Dict[str, User] = {host.id: host}
        self.host = host.id
        self.id:str = str(uuid.uuid4())
        self.state:GameState = GameState.WAITING_FOR_PLAYER

    def join(self, playername:str):
        self.player = User(playername)
        self.state = GameState.READY

    def play(self, user_id:str, choice:Hand):
        if self.state == GameState.READY:
            self.state = GameState.WAITING_FOR_ACTION
        elif self.state == GameState.WAITING_FOR_ACTION:
            self.state = GameState.READY



class Round(Game):
    hosthand:Hand = Hand.UNSET
    playerhand:Hand = Hand.UNSET
    
    def __init__(self):
        pass
   

