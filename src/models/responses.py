from pydantic import BaseModel


class UserResponse(BaseModel):
    token:str
    game:str

class GamesResponse(BaseModel):
    name:str
    id:str

class StateResponse(BaseModel):
    state: int