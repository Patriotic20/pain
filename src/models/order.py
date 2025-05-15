from sqlalchemy import Column , String , Integer , ForeignKey , Enum as SqlEnum
from sqlalchemy.orm import relationship
from src.core.base import Base
from enum import Enum

class OrderTime(Base):
    __tablename__ = "order_times"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(String)
    end_time = Column(String)

    user   = relationship("User", back_populates="order_times")
    orders = relationship("Order", back_populates="order_time", cascade="all,delete-orphan")


class OrderStatus(str, Enum):
    free        = "free"
    booked      = "booked"
    in_progress = "in_progress"
    completed   = "completed"
    cancelled   = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    lab_analis_id = Column(Integer, ForeignKey("lab_analis.id"), nullable=False)
    order_time_id = Column(Integer, ForeignKey("order_times.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column( SqlEnum(OrderStatus), default=OrderStatus.free)

    lab_analis = relationship("LabAnalis", back_populates="orders")
    order_time = relationship("OrderTime", back_populates="orders")
    user = relationship("User", back_populates="orders")
