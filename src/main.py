from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import debugpy
from pydantic import BaseModel

from src.models.Game import Game
from src.repositories.gameRepository import GameRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    app.game_repo = GameRepository()
    yield
    print('Shut down')


app = FastAPI(lifespan=lifespan)

class UserRequest(BaseModel):
    name: str

class UserResponse(BaseModel):
    token:str


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


@app.post("/host")
async def host(host:UserRequest):
    game:Game = Game(host.name)
   
    success:bool = app.game_repo.save_game(game)
    if success:
        return {"token": str(game.host.id), "game": str(game.id)}
    else:
        return {"token": "Jackshit"}
    


    


if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
    uvicorn.run("src.main:app",  host="0.0.0.0", port=8000, log_level="debug", reload=True)
    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("Debugged attached")