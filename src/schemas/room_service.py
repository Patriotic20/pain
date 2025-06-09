from pydantic import BaseModel


class RoomServiceBase(BaseModel):
    room_id: int
    service_id: int


class RoomServiceCreate(RoomServiceBase):
    price: str


class LabAnalisResponse(RoomServiceCreate):
    id: int


class RoomServiceUpdate(BaseModel):
    service_id: int | None = None
    price: str | None | None
