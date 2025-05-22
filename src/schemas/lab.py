from pydantic import BaseModel


class LabBase(BaseModel):
    name: str
    description: str


class LabUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class LabResponse(LabBase):
    id: int


class UserLabCreate(BaseModel):
    user_id: int
    lab_id: int
