from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import debugpy


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    yield
    print('Shut down')


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello, world!"}


if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")
    uvicorn.run("src.main:app",  host="0.0.0.0", port=8000, log_level="debug", reload=True)
    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("Debugged attached")