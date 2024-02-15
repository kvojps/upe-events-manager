from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthCheckResponse(BaseModel):
    status: str


@router.get("")
def health_check():
    return HealthCheckResponse(status="Ok")
