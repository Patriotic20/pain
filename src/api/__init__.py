from fastapi import APIRouter

from .auth import auth_router
from .lab import lab_router
from .room_service import room_service_router
from .order import order_router
from .room import room_router
from .service import service_router
from .time_slot import time_slot_router

api_router = APIRouter(prefix="/api")


api_router.include_router(auth_router)
api_router.include_router(lab_router)
api_router.include_router(room_router)
api_router.include_router(service_router)
api_router.include_router(room_service_router)
api_router.include_router(time_slot_router)
api_router.include_router(order_router)
