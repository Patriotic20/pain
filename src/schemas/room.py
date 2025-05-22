from pydantic import BaseModel


class RoomBase(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str

class RoomCreate(RoomBase):
    lab_id: int

class RoomUpdate(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str