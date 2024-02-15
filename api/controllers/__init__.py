from fastapi import APIRouter
from .event import router as event_router
from .health_check import router as health_check_router

main_router = APIRouter()

main_router.include_router(
    health_check_router, prefix="/health_check", tags=["Health check"]
)

main_router.include_router(event_router, prefix="/events", tags=["Events"])
