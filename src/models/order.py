from enum import Enum
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship
from src.core.base import Base

class OrderStatus(str, Enum):
    free = "free"
    booked = "booked"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    room_service_id = Column(Integer, ForeignKey("room_services.id"))
    time_slot_id = Column(Integer, ForeignKey("time_slots.id"))
    discount = Column(String)
    customer_id = Column(Integer , ForeignKey("users.id"))
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.free)

    room_service = relationship("RoomService", back_populates="orders")
    time_slot = relationship("TimeSlot", back_populates="orders")
    users = relationship("User", back_populates="orders")