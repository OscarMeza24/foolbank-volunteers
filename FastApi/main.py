from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return ("Hello World")

@app.get("/id/{id}")
async def read_url(id: int):
    suma = id + 10
    return (suma)