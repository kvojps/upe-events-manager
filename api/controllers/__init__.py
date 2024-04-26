from fastapi import APIRouter, Depends
from api.security import is_valid_token
from .auth import router as auth_user_route
from .event import router as event_router
from .health_check import router as health_check_router
from .paper import router as paper_router
from .subscriber import router as subscriber_router

main_router = APIRouter()

main_router.include_router(
    auth_user_route,
    prefix="/auth",
    tags=["Authentication"],
)

main_router.include_router(
    health_check_router,
    prefix="/health_check",
    tags=["Health check"],
    dependencies=[Depends(is_valid_token)],
)

main_router.include_router(event_router, prefix="/events", tags=["Events"])

main_router.include_router(paper_router, prefix="/papers", tags=["Papers"])

main_router.include_router(subscriber_router, prefix="/subscribers", tags=["Subscribers"])
