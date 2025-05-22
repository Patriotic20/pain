from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from src.core.base import Base


class LabService(Base):
    __tablename__ = "lab_services"

    id = Column(Integer, primary_key=True)
    lab_id = Column(Integer, ForeignKey("labs.id"), nullable=False)
    services_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    price = Column(String, nullable=False)

    lab = relationship("Lab", back_populates="lab_services_links")
    services = relationship("Service", back_populates="lab_services_links")
    orders = relationship(
        "Order", back_populates="lab_services", cascade="all, delete-orphan"
    )
