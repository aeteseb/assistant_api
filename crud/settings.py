from sqlalchemy.orm import Session
from .. import schemas
from .. import models


def get_user_settings(user_id: int, db: Session) -> models.Settings:
    result = db.query(models.Settings).filter(models.Settings.id == user_id).first()
    if result is None:
        return create_user_settings(db, user_id)
    return result


def set_user_setting(
    user_id: int, setting: schemas.Setting, db: Session
) -> schemas.Setting | None:
    db_settings = get_user_settings(user_id, db)
    print(db_settings.theme_mode)
    if db_settings is None:
        return None
    if not hasattr(db_settings, setting.key):
        return None
    setattr(db_settings, setting.key, setting.value)
    db.commit()
    db.refresh(db_settings)
    return setting


def create_user_settings(db: Session, user_id: int):
    db_settings = models.Settings(
        id=user_id,
    )
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings
