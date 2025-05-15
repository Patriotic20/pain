from pydantic import BaseModel

class LabBase(BaseModel):
    name: str
    description: str


class LabUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    
class LabCreate(LabBase):
    user_id: int


class LabResponse(LabBase):
    id: int