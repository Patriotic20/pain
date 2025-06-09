from sqlalchemy import ARRAY, Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tags = Column(ARRAY(String))

    room_services = relationship("RoomService", back_populates="service", cascade="all, delete-orphan")