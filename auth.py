import os
from datetime import datetime, timedelta
from typing import Annotated, Literal
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from .schemas.users import User, UserInDB, fake_users_db

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the plain password matches the hashed password.

    Args:
        plain_password (str): The plain password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Returns the hashed password.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def get_user(db, username: str) -> UserInDB | None:
    """
    Returns the user with the specified username.

    Args:
        db (dict): The database of users.
        username (str): The username of the user to return.

    Returns:
        UserInDB | None: The user with the specified username, or None if no user has the specified username.
    """
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

    return None


def authenticate_user(db, username: str, password: str) -> UserInDB | None:
    """
    Authenticates the user with the specified username and password.

    Args:
        db (dict): The database of users.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        UserInDB | None: The user with the specified username and password, or None if no user has the specified username or the password is incorrect.
    """
    user = get_user(db, username)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates an access token.

    Args:
        data (dict): The data to store in the access token.
        expires_delta (int | None): The number of seconds until the access token expires.

    Returns:
        str: The access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Returns the current user.

    Args:
        token (str): The access token.

    Returns:
        User: The current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception  # pylint: disable=raise-missing-from

    if token_data.username is None:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception

    return User(**user.model_dump(exclude={"hashed_password"}))


def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    """
    Returns the current active user.

    Args:
        current_user (User): The current user.

    Returns:
        User: The current active user.

    Raises:
        HTTPException: If the current user is disabled.
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user
