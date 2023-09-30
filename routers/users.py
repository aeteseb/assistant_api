from typing import Annotated
from ..schemas.users import User

from fastapi import APIRouter, Depends

from ..auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


# todo: make admin only
@router.get("/")
async def get_users():
    """
    Returns a list of users.

    Returns:
        list: A list of users.
    """
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def get_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Returns the current authenticated user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user.
    """
    return current_user


# todo make admin only
@router.get("/{username}")
async def get_user(username: str):
    """
    Returns a specific user.

    Args:
        username (str): The username of the user to return.

    Returns:
        dict: A JSON object with a "username" key and the value of the username argument.
    """
    return {"username": username}
