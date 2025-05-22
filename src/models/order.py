from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from src.core.base import Base
from enum import Enum


class OrderStatus(str, Enum):
    free = "free"
    booked = "booked"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    lab_service_id = Column(Integer, ForeignKey("lab_services.id"))
    time_slot_id = Column(Integer, ForeignKey("time_slots.id"))
    discount = Column(String)
    customer_id = Column(Integer)
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.free)

    lab_services = relationship("LabService", back_populates="orders")
    time_slot = relationship("TimeSlot", back_populates="orders")
