from pydantic import BaseModel


class AnalisBase(BaseModel):
    name: str


class AnalisUpdate(BaseModel):
    name: str | None = None


class AnalisResponse(AnalisBase):
    id: int
