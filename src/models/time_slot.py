from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.core.base import Base

class TimeSlot(Base):
    __tablename__ = "time_slots"

    id = Column(Integer, primary_key=True)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"))

    room = relationship("Room", back_populates="time_slots")
    orders = relationship("Order", back_populates="time_slot", cascade="all, delete-orphan")