from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from . import models
from .routers import users, auth, meal_plan
from .database import engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(meal_plan.router)


@app.get("/")
async def root():
    """
    Returns a JSON object with a "message" key and the value "Hello World".

    Returns:
        dict: A JSON object with a "message" key and the value "Hello World".
    """
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
