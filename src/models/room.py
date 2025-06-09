from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.core.base import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    lab_id = Column(Integer, ForeignKey("labs.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

    lab = relationship("Lab", back_populates="rooms")
    time_slots = relationship("TimeSlot", back_populates="room", cascade="all, delete-orphan")
    room_services = relationship("RoomService", back_populates="room", cascade="all, delete-orphan")