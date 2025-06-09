from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import DECIMAL
from sqlalchemy.orm import relationship
from src.core.base import Base

class RoomService(Base):
    __tablename__ = "room_services"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    price = Column(String, nullable=False)

    room = relationship("Room", back_populates="room_services")
    service = relationship("Service", back_populates="room_services")
    orders = relationship("Order", back_populates="room_service", cascade="all, delete-orphan")