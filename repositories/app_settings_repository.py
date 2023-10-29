from fastapi import HTTPException
from sqlalchemy.orm import Session
from .. import schemas
from .. import models


def get_user_settings(user_id: int, db: Session) -> schemas.AppSettings:
    result = (
        db.query(schemas.AppSettings).filter(schemas.AppSettings.id == user_id).first()
    )
    if result is None:
        raise HTTPException(status_code=404, detail="User settings not found")
    return result


def set_user_setting(
    user_id: int, setting: models.Setting, db: Session
) -> models.Setting | None:
    db_settings = get_user_settings(user_id, db)
    if db_settings is None:
        return None
    if not hasattr(db_settings, setting.key):
        return None
    setattr(db_settings, setting.key, setting.value)
    db.commit()
    db.refresh(db_settings)
    return setting


def create_app_settings(db: Session, user_id: int, settings: models.AppSettingsCreate):
    db_settings = schemas.AppSettings(
        id=user_id,
        theme_mode=settings.theme_mode,
        theme_color=settings.theme_color,
    )
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings