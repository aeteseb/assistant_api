from fastapi import FastAPI

from .routers import users

app = FastAPI()

app.include_router(users.router)


@app.get("/")
async def root():
    """
    Returns a JSON object with a "message" key and the value "Hello World".

    Returns:
        dict: A JSON object with a "message" key and the value "Hello World".
    """
    return {"message": "Hello World"}
