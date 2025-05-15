from fastapi import APIRouter
from .auth import auth_router
from .lab import lab_router
from .analis import analis_router
from .lab_analis import lab_analis_router
from .order_time import order_time_router

api_router = APIRouter(
    prefix="/api"
)


api_router.include_router(auth_router)
api_router.include_router(lab_router)
api_router.include_router(analis_router)
api_router.include_router(lab_analis_router)
api_router.include_router(order_time_router)
