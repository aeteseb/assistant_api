from datetime import datetime
from sqlalchemy.orm import Session
from .. import schemas
from .. import models


def get_meal_plans(
    db: Session,
    user_id: int,
    start_date: datetime,
    end_date: datetime,
):
    return (
        db.query(models.MealPlan)
        .filter(
            models.MealPlan.user_id == user_id,
            models.MealPlan.date >= start_date,
            models.MealPlan.date <= end_date,
        )
        .all()
    )
