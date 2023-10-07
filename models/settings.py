from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    theme_mode = Column(String, default="system")
    theme_color = Column(String, default="lime")

    user = relationship("User", back_populates="settings")
