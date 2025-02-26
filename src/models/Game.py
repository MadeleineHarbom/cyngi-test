from typing import Optional
import uuid

class Game:
    def __init__(self, hostname:str):
        self.host:User = User(hostname)
        self.player:Optional[User] = None
        self.id:str = str(uuid.uuid4())

    def join(self, playername:str):
        self.player = User(playername)

    def __str__(self):
        return f"Game(id={self.id}, host=User(id={self.host.id}, {self.host.name}), player=User(id={self.player.id}, {self.player.name}))" if self.player else f"Game(id={self.id}, host=User(id={self.host.id}, {self.host.name}))"

class User(Game):
    def __init__(self, name:str):
        self.id:str = str(uuid.uuid4()) 
        self.name:str = name

