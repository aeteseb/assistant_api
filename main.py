from fastapi import FastAPI
from dotenv import load_dotenv

from .routers import users, auth

load_dotenv()
app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    """
    Returns a JSON object with a "message" key and the value "Hello World".

    Returns:
        dict: A JSON object with a "message" key and the value "Hello World".
    """
    return {"message": "Hello World"}
