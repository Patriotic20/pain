from pydantic import BaseModel


class LabAnalisBase(BaseModel):
    lab_id: int
    analysis_id: int


class LabAnalisCreate(LabAnalisBase):
    price: str


class LabAnalisResponse(LabAnalisCreate):
    id: int


class LabAnalisUpdate(BaseModel):
    analysis_id: int | None = None
    price: str | None = None
