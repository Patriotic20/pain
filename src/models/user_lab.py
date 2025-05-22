from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.core.base import Base


class UserLab(Base):
    __tablename__ = "user_labs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lab_id = Column(Integer, ForeignKey("labs.id"))

    user = relationship("User", back_populates="user_labs")
    lab = relationship("Lab", back_populates="user_labs")
