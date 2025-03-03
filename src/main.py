from configparser import Error
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Header
from contextlib import asynccontextmanager
from transitions import MachineError
import uvicorn
import debugpy

from src.models.player import Player
from src.models.game import Game
from src.models.requests import PlayRequest, UserRequest
from src.models.responses import GamesResponse, StateResponse, UserResponse
from src.repositories.gameRepository import GameRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    yield
    print('Shut down')

app = FastAPI(lifespan=lifespan)


@app.get('/games')
async def get_games(repo:GameRepository=Depends(GameRepository)) -> List[GamesResponse]:
    try:
        games:List[Game] = repo.get_available_games()
        return [{'id': game.id, 'name': game.get_host_name()} for game in games]
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error')


@app.post('/host')
async def host(host:UserRequest, repo:GameRepository=Depends(GameRepository) )-> UserResponse:
    try:
        host:Player = Player(host.name)
        game:Game = Game(host)
        repo.save_game(game)
        return UserResponse(token=host.id, game= game.id)
    except:
        raise HTTPException(status_code=500, detail='Internal Server Error')
    
    
@app.post('/join/{game_id}')
async def join(game_id:str ,player:UserRequest, repo:GameRepository=Depends(GameRepository)) -> UserResponse:
    try:
        game:Game = repo.get_game_by_id(game_id)
        user:Player = Player(player.name)
        game.join(user)
        return {'token': str(user.id), 'game': game.id}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post('/play/{game_id}')
async def play(game_id:str, body:PlayRequest, token: str = Header(None), repo:GameRepository=Depends(GameRepository)):
    if token is None:
        raise HTTPException(status_code=400, detail='Token is required')
    try:
        hand:int = body.move
        game:Game = repo.get_game_by_id(game_id)
        play:Optional[str] = game.play(token,hand)
        #TODO fix this
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    

@app.get('/state/{game_id}')
async def state(game_id:str,  repo:GameRepository=Depends(GameRepository)) -> StateResponse:
    try:
        game:Game = repo.get_game_by_id(game_id)
        return {'state': game.state}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@app.post('/leave/{game_id}')
async def play(game_id:str,  token: str = Header(None), repo:GameRepository=Depends(GameRepository)):
    if token is None:
        raise HTTPException(status_code=400, detail='Token is required')
    try:
        game:Game = repo.get_game_by_id(game_id)
        game.leave(token)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except MachineError as e:
        raise HTTPException(status_code=403, detail= 'Cannot leave as this time')
    

if __name__ == '__main__':
    #uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='debug')
    uvicorn.run('src.main:app',  host='0.0.0.0', port=8000, log_level='debug', reload=True)
    debugpy.listen(('0.0.0.0', 5678))
    print('Waiting for debugger to attach...')
    debugpy.wait_for_client()
    print('Debugged attached')