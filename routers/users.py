from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users():
    """
    Returns a list of users.

    Returns:
        list: A list of users.
    """
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def get_user_me():
    """
    Returns the current user.

    Returns:
        dict: A JSON object with a "username" key and the value "fakecurrentuser".
    """
    return {"username": "fakecurrentuser"}


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
