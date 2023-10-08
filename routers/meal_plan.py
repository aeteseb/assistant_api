from datetime import datetime
from fastapi import APIRouter, Depends
from ..schemas import User
from ..auth import get_current_active_user
from ..database import get_db
from .. import schemas
from .. import crud


router = APIRouter(tags=["Food", "Meal Plan"], prefix="/mealplans")


@router.get("/", response_model=list[schemas.MealPlan])
async def get_meal_plans(
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(get_current_active_user),
    db=Depends(get_db),
):
    """
    Returns a list of meal plans.

    Returns:
        list: A list of meal plans.
    """
    return crud.get_meal_plans(
        db, current_user.id, start_date=start_date, end_date=end_date
    )
