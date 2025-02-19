from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    yield
    print('Shut down')


app = FastAPI(lifespan=lifespan)


class HostRequest(BaseModel):
    name: str


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


