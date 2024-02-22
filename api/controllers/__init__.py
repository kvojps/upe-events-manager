from fastapi import APIRouter, Depends

from api.security import token_verifier
from .event import router as event_router
from .health_check import router as health_check_router
from .paper import router as paper_router
from .auth_user import router as auth_user_route

main_router = APIRouter()

main_router.include_router(
    auth_user_route,
    prefix="/auth",
    tags=["User authentication"],
)

main_router.include_router(
    health_check_router,
    prefix="/health_check",
    tags=["Health check"],
    dependencies=[Depends(token_verifier)],
)

main_router.include_router(event_router, prefix="/events", tags=["Events"])

main_router.include_router(paper_router, prefix="/papers", tags=["Papers"])
