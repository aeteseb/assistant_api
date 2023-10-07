from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session

from .. import crud
from ..schemas import UserCreate
from ..auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from ..database import get_db

router = APIRouter(tags=["authentication"])


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


class OAuth2SignupForm(OAuth2PasswordRequestForm):
    email: EmailStr | None = None
    full_name: str | None = None


@router.post("/signup", response_model=Token)
async def signup_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    email: Annotated[EmailStr, Body()],
    full_name: Annotated[str | None, Body()] = None,
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
    crud.create_user(
        db,
        UserCreate(
            username=form_data.username,
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        ),
    )
    return await login_for_access_token(form_data, db)
