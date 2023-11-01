from assistant_api import schemas
from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

import assistant_api.routers.auth_router as auth
import assistant_api.routers.settings_router as settings

from .core.database import engine

load_dotenv()

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(settings.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
