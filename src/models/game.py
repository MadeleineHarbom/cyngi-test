from typing import Dict, List, Optional
import uuid
from src.constants.states import GameState
from src.constants.hands import Hand
from src.models.player import Player
from transitions import Machine, State

class Game:
    def __init__(self, host:Player):
        self.users:Dict[str, Player] = {host.id: host}
        self.host = host.id
        self.id:str = str(uuid.uuid4())
        #self._state:GameState = GameState.WAITING_FOR_PLAYER
        self.previous_rounds:List[Round] = []
        self.active_round = None

        states:List[str] = [state.value for state in GameState]
        self.machine= Machine(model=self, states=states, initial=GameState.WAITING_FOR_PLAYER.value)

        self.machine.add_transition('join_game', GameState.WAITING_FOR_PLAYER.value, GameState.READY.value)
        self.machine.add_transition('play_hand', GameState.READY.value, GameState.WAITING_FOR_ACTION.value)
        self.machine.add_transition('play_hand', GameState.WAITING_FOR_ACTION.value, GameState.READY.value)
        self.machine.add_transition('leave_game', GameState.WAITING_FOR_PLAYER.value, GameState.TEMINATED.value)
        self.machine.add_transition('leave_game', GameState.READY.value, GameState.COMPLETED.value)


    def join(self, player:Player):
        self.users[player.id] = player
        self.trigger('join_game') 
        #self._state = GameState.READY


    def validate_user(self, user_id):
        try:
            self.users[user_id]
        except:
            raise PermissionError('User not in game')
        
    
    def get_host_name(self) -> str:
        return self.users.get(self.host).name

    def play(self, user_id:str, choice:Hand) -> Optional[str]:
        self.validate_user(user_id)
        if self.state == GameState.READY.value:
            self.active_round = Round(user_id, choice)
            self.trigger('play_hand')
        elif self.state == GameState.WAITING_FOR_ACTION.value:
            played:bool = self.active_round.play(user_id, choice)
            if played:
                winner_id:str = self.active_round.winner
                self.previous_rounds.append(self.active_round)
                self.active_round = None
                self.trigger('play_hand')
                return winner_id



    def leave(self, user_id:str) -> bool:
        self.validate_user(user_id)
        self.trigger('leave_game')
        return True

class Round: 
    def __init__(self, user_id: str, choice:Hand):
        self.hands:Dict[str, Hand] = {user_id: choice}
        self.winner = None
   

    def play(self, user_id:str, hand:Hand) -> bool:
        if self._validate_user(user_id):
            self.hands[user_id] = hand
            self.winner = self._set_winner()
            return True
        return False


    def _set_winner(self) -> str:
        (player1, player2), (hand1, hand2) = self.hands.keys(), self.hands.values()
        if hand1 == hand2:
            return ''
        if hand1 == Hand.PAPER and hand2 == Hand.ROCK:
            return player1
        if hand1 == Hand.ROCK and hand2 == Hand.SCISSORS:
            return player1
        if hand1 == Hand.SCISSORS and hand2 == Hand.PAPER:
            return player1
        if hand1 == Hand.PAPER and hand2 == Hand.SCISSORS:
            return player2
        if hand1 == Hand.ROCK and hand2 == Hand.PAPER:
            return player2
        if hand1 == Hand.SCISSORS and hand2 == Hand.ROCK:
            return player2
        

    def _validate_user(self, user_id:str) -> bool:
        if self.hands.get(user_id, None):
            raise PermissionError('User already played this turn')
        else:
            return True



