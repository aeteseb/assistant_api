from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires: datetime


class TokenData(BaseModel):
    username: str | None = None
