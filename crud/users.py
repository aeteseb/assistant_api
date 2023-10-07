from sqlalchemy.orm import Session
from .. import schemas
from .. import models


def get_user(db: Session, user_id: int):
    """
    Returns the user with the specified ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to return.

    Returns:
        User | None: The user with the specified ID, or None if no user has the specified ID.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Returns the user with the specified email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to return.

    Returns:
        User | None: The user with the specified email, or None if no user has the specified email.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """
    Returns the user with the specified username.

    Args:
        db (Session): The database session.
        username (str): The username of the user to return.

    Returns:
        User | None: The user with the specified username, or None if no user has the specified username.
    """
    result = db.query(models.User).filter(models.User.username == username).first()
    print(result)
    result = db.query(models.User).all()
    print(result)
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns a list of users.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of users to skip. Defaults to 0.
        limit (int, optional): The maximum number of users to return. Defaults to 100.

    Returns:
        list: A list of users.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a user.

    Args:
        db (Session): The database session.
        user (UserCreate): The user to create.

    Returns:
        User: The created user.
    """
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=user.hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
