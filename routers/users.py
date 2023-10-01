from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..auth import get_current_active_user
from ..database import get_db
from ..schemas import Setting, Settings, User, UserCreate

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


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


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


@router.get("/me/settings", tags=["settings"])
async def get_user_settings(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Settings:
    """
    Returns the current authenticated user's settings.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user's settings.
    """
    settings = crud.get_user_settings(current_user.id, db)
    return settings


@router.get("/me/settings/{setting_name}", tags=["settings"])
async def get_user_setting_from_name(
    setting_name: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int | str | bool]:
    """
    Returns the current authenticated user's settings.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user's settings.
    """
    settings = crud.get_user_settings(current_user.id, db)
    response = settings.model_dump(include={setting_name})
    if not response:
        raise HTTPException(status_code=404, detail="Setting does not exist")
    return response


@router.patch("/me/setting", tags=["settings"])
async def patch_user_setting(
    setting: Setting,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Setting:
    """
    Returns the current authenticated user's settings.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user's settings.
    """
    response = crud.set_user_setting(
        db=db,
        user_id=current_user.id,
        setting=setting,
    )
    if not response:
        raise HTTPException(status_code=404, detail="Setting does not exist")
    return response


def _set_setting_helper(
    db: Session,
    user_id: int,
    setting: Setting,
) -> Setting | None:
    response = crud.set_user_setting(
        db=db,
        user_id=user_id,
        setting=setting,
    )
    if not response:
        raise HTTPException(status_code=404, detail=f"Setting {setting} does not exist")
    return setting


@router.patch("/me/settings/all", tags=["settings"])
async def patch_all_user_settings(
    settings: Settings,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Settings:
    """
    Returns the current authenticated user's settings.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user's settings.
    """
    for setting, value in settings.model_dump().items():
        _set_setting_helper(db, current_user.id, Setting(key=setting, value=value))
    return settings


@router.patch("/me/settings", tags=["settings"])
async def patch_some_user_settings(
    settings: list[Setting],
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Settings:
    """
    Returns the current authenticated user's settings.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current authenticated user's settings.
    """
    for setting in settings:
        _set_setting_helper(db, current_user.id, setting)
    return crud.get_user_settings(current_user.id, db)


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
