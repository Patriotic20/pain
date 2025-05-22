from pydantic import BaseModel , Field
from typing import List 

class ServiceBase(BaseModel):
    name: str
    description: str
    tags: List[str] = Field(default_factory=list)


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    tags: List[str] = Field(default_factory=list)