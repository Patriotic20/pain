from sqlalchemy import Column, String, Integer, ARRAY
from sqlalchemy.orm import relationship
from src.core.base import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tags = Column(ARRAY(String))

    lab_services_links = relationship(
        "LabService", back_populates="services", cascade="all,delete-orphan"
    )
    labs = relationship("Lab", secondary="lab_services", back_populates="services")
