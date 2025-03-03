from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str


class PlayRequest(BaseModel):
    move: int