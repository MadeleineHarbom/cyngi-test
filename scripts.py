import uvicorn

def dev():
    print("dev starting")
    uvicorn.run("src.main:app", reload=True)