from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    labs = relationship("Lab", secondary="user_labs", back_populates="users", overlaps="user_labs,lab")
    user_labs = relationship("UserLab", back_populates="user", cascade="all, delete-orphan", overlaps="labs,lab")
    orders = relationship("Order", back_populates="users")
