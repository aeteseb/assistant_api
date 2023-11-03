from typing import Annotated
from assistant_api.core.auth import get_current_active_user
from assistant_api.core.database import get_db
from assistant_api.models.app_settings_models import AppSettingsCreate
from assistant_api.models.user_models import User
from fastapi import APIRouter, Depends
import assistant_api.repositories.app_settings_repository as settings_repo
from sqlalchemy.orm import Session


router = APIRouter(prefix="/settings", tags=["authentication"])


@router.post("")
async def set_settings(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_active_user)],
    settings: AppSettingsCreate,
) -> AppSettingsCreate:
    """
    Sets the user's settings.

    Args:
        user (User): The user.
        settings (dict): The settings.

    Returns:
        dict: The settings.
    """
    saved_settings = settings_repo.set_app_settings(
        db,
        user.id,
        settings,
    )
    if saved_settings is None:
        saved_settings = settings_repo.create_app_settings(
            db,
            user.id,
            settings,
        )
    return saved_settings
