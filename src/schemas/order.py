from pydantic import BaseModel
from src.models.order import OrderStatus


class OrderBase(BaseModel):
    room_service_id : int
    discount : str



class OrderUpdata(BaseModel):
    customer_id: int
    status: OrderStatus