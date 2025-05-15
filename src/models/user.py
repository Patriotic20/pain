from sqlalchemy import Column , Integer , String
from src.core.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    labs = relationship("Lab", back_populates="user", cascade="all,delete-orphan")
    order_times = relationship("OrderTime", back_populates="user", cascade="all,delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all,delete-orphan")
