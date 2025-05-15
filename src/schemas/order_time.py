from pydantic import BaseModel

class OrderTimeBase(BaseModel):
    start_time: str
    end_time: str


class OrderTimeCreate(OrderTimeBase):
    user_id: int


class OrderTimeResponse(OrderTimeCreate):
    id: int

class OrderTimeUpdate(BaseModel):
    start_time: str | None = None
    end_time: str | None = None