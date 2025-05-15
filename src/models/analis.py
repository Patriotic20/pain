from sqlalchemy import Column , String , Integer
from sqlalchemy.orm import relationship
from src.core.base import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id    = Column(Integer, primary_key=True)
    name  = Column(String,  nullable=False)


    lab_analis_links = relationship(
                            "LabAnalis",
                            back_populates="analysis",
                            cascade="all,delete-orphan"
                        )

    labs = relationship(
        "Lab",
        secondary="lab_analis",
        back_populates="analises"
    )