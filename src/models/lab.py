from sqlalchemy import Column , String , Integer , ForeignKey
from src.core.base import Base
from sqlalchemy.orm import relationship

class Lab(Base):
    __tablename__ = "labs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String,  nullable=False)
    description = Column(String,  nullable=False)

    user = relationship("User",      back_populates="labs")
    lab_analis_links = relationship("LabAnalis", back_populates="lab", cascade="all,delete-orphan")

    analises = relationship(
        "Analysis",
        secondary="lab_analis",
        back_populates="labs"
    )