from assistant_api import schemas
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

import assistant_api.routers.auth_router as auth

from .core.database import engine

load_dotenv()

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
