from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.core.base import Base


class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    lab_services_links = relationship(
        "LabService", back_populates="lab", cascade="all,delete-orphan"
    )
    services = relationship("Service", secondary="lab_services", back_populates="labs")
    users = relationship("User", secondary="user_labs", back_populates="labs")
    user_labs = relationship(
        "UserLab", back_populates="lab", cascade="all, delete-orphan"
    )
    rooms = relationship("Room", back_populates="lab", cascade="all, delete-orphan")
