from datetime import datetime
import enum
from pydantic import BaseModel


class MealType(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"


class MealBase(BaseModel):
    name: str
    description: str | None = None
    meal_type: MealType


class MealCreate(MealBase):
    pass


class Meal(MealBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class MealPlanBase(BaseModel):
    date: datetime
    meal_type: MealType
    breakfast: Meal | None = None
    lunch: Meal | None = None
    dinner: Meal | None = None
    snacks: list[Meal] | None = None


class MealPlanCreate(MealPlanBase):
    pass


class MealPlan(MealPlanBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
