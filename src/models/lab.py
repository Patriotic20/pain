from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.base import Base

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    users = relationship("User", secondary="user_labs", back_populates="labs", overlaps="user_labs,user")
    user_labs = relationship("UserLab", back_populates="lab", cascade="all, delete-orphan", overlaps="users,user")
    rooms = relationship("Room", back_populates="lab", cascade="all, delete-orphan")
