from sqlalchemy import Column , Integer , ForeignKey , String
from src.core.base import Base
from sqlalchemy.orm import relationship

class LabAnalis(Base):
    __tablename__ = "lab_analis"

    id            = Column(Integer, primary_key=True)
    lab_id        = Column(Integer, ForeignKey("labs.id"),      nullable=False)
    analysis_id   = Column(Integer, ForeignKey("analyses.id"),  nullable=False)
    price         = Column(String,  nullable=False)

    # now explicit back_populates
    lab        = relationship("Lab",      back_populates="lab_analis_links")
    analysis   = relationship("Analysis", back_populates="lab_analis_links")
    orders     = relationship("Order",     back_populates="lab_analis")




