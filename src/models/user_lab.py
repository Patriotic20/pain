from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from src.core.base import Base

class UserLab(Base):
    __tablename__ = "user_labs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lab_id = Column(Integer, ForeignKey("labs.id"))

    user = relationship("User", back_populates="user_labs", overlaps="labs")
    lab = relationship("Lab", back_populates="user_labs", overlaps="users")
