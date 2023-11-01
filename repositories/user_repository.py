from sqlalchemy.orm import Session
from .. import schemas
from .. import models


def get_user(db: Session, user_id: int) -> models.User | None:
    """
    Returns the user with the specified ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to return.

    Returns:
        User | None: The user with the specified ID, or None if no user has the specified ID.
    """
    return db.query(schemas.User).filter(schemas.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User | None:
    """
    Returns the user with the specified username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to return.

    Returns:
        User | None: The user with the specified username, or None if no user has the specified username.
    """
    result = db.query(schemas.User).filter(schemas.User.username == username).first()
    print(result)
    result = db.query(schemas.User).all()
    return db.query(schemas.User).filter(schemas.User.username == username).first()


def create_user(db: Session, user: models.UserCreate) -> models.User:
    """
    Creates a user.

    Args:
        db (Session): The database session.
        user (UserCreate): The user to create.

    Returns:
        User: The created user.
    """
    db_user = schemas.User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        emoji=user.emoji,
        hashed_password=user.hashed_password,
        is_active=True,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
