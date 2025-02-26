from typing import List
from fastapi import Depends, FastAPI, HTTPException
from contextlib import asynccontextmanager
import uvicorn
import debugpy
from pydantic import BaseModel

from src.interfaces.singleton import singleton
from src.models import GameList
from src.models.Game import Game
from src.repositories.gameRepository import GameRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    yield
    print('Shut down')


app = FastAPI(lifespan=lifespan)

class UserRequest(BaseModel):
    name: str

class UserResponse(BaseModel):
    token:str
    game:str

#class GamesResponse(BaseModel):
#    games:List[Game]

@app.get("/")
async def get_root():
    return {"message": "Hello, world!"}


@app.get("/games")
async def get_games(repo:GameRepository=Depends(GameRepository)):
    repo:GameRepository = GameRepository()
    games:GameList = repo.get_available_games()
    return {"games": games}



@app.post("/host")
async def host(host:UserRequest, repo:GameRepository=Depends(GameRepository) )-> UserResponse:
    game:Game = Game(host.name)
    print(game)
    print(game.id)
    success:bool = repo.save_game(game)
    if success:
        return UserResponse(token=game.host.id, game= game.id)
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.post("/join/{game_id}")
async def join(game_id:str ,player:UserRequest, repo:GameRepository=Depends(GameRepository)) -> UserResponse:
    game:Game = repo.get_game_by_id(game_id)
    game.join(player.name)
    return {"token": str(game.player.id), "game": str(game.id)}

    

if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
    uvicorn.run("src.main:app",  host="0.0.0.0", port=8000, log_level="debug", reload=True)
    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("Debugged attached")