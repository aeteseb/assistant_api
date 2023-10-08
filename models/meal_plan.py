from sqlalchemy import Column, Integer, String

from ..database import Base


class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    meal_type = Column(String)
    user_id = Column(Integer, index=True)


class MealPlan(Base):
    __tablename__ = "mealplans"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    meal_type = Column(String)
    breakfast = Column(Integer, nullable=True)
    lunch = Column(Integer, nullable=True)
    dinner = Column(Integer, nullable=True)
    snacks = Column(String, nullable=True)
    user_id = Column(Integer, index=True)
