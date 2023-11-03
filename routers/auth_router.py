from datetime import datetime, timedelta
from typing import Annotated
from assistant_api.core.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)
from assistant_api.core.database import get_db
from assistant_api.models.token_models import Token
from assistant_api.models.user_models import User, UserCreate
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from ..repositories import user_repository as user_repo

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    """
    Returns an access token.

    Args:
        form_data (dict[str, str]): The form data.

    Returns:
        Token: The access token.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires=datetime.today() + access_token_expires,
    )


@router.post("/signup", response_model=Token)
async def signup_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    email: Annotated[EmailStr | None, Body()] = None,
    first_name: Annotated[str | None, Body()] = None,
    last_name: Annotated[str | None, Body()] = None,
    emoji: Annotated[str | None, Body()] = None,
) -> Token:
    """
    Returns an access token.

    Args:
        form_data (dict[str, str]): The form data.

    Returns:
        Token: The access token.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    hashed_password = get_password_hash(form_data.password)
    user_repo.create_user(
        db,
        UserCreate(
            username=form_data.username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            emoji=emoji,
            hashed_password=hashed_password,
        ),
    )

    return await login_for_access_token(form_data, db)


@router.post("/validate-username")
async def validate_username(
    username: Annotated[str, Body()],
    db: Annotated[Session, Depends(get_db)],
) -> bool:
    """
    Returns whether the username is valid.

    Args:
        username (str): The username to validate.

    Returns:
        bool: Whether the username is valid.
    """
    return user_repo.get_user_by_username(db, username) is None


@router.get("/user-id")
async def get_user_id(
    user: Annotated[User, Depends(get_current_active_user)],
) -> int:
    return user.id
