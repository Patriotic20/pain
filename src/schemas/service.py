
from pydantic import BaseModel, Field


class ServiceBase(BaseModel):
    name: str
    description: str
    tags: list[str] = Field(default_factory=list)


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)


class LabService(BaseModel):
    lab_id: int
    services_id: int
