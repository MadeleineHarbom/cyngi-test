from typing import Optional
import uuid

class Game:
    def __init__(self, hostname:str):
        self.host:User = User(hostname)
        self.player:Optional[User] = None
    
class User(Game):
    def __init__(self, name:str):
        self.id:uuid = uuid.uuid4() 
        self.name:str = name

