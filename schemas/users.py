from pydantic import BaseModel

fake_users_db = {
    "rick": {
        "username": "rick",
        "full_name": "Rick Sanchez",
        "email": "rick@example.com",
        "hashed_password": "$2b$12$1kicK/InmKhp6Xkk4vk6/u9k4dcccqpewv0RYU5N7p8C/5yx.ciKy",
        "disabled": False,
    },
}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
