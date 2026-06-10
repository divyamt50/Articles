from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Engine room has power"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"greeting": f"Hey {name} welcome back"}


@app.get("/ping")
async def ping():
    return {"status":"ok"}

@app.get("/check/{id}")
def check(id:int):
    return {"user_id":id, "status":"active"}