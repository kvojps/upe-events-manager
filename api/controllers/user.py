from fastapi import APIRouter, Depends, HTTPException, Query
from api.contracts.responses.user import UserResponse
from api.models.dto.user import UserDTO
from core.infrastructure.settings.security import is_super_user
from api.contracts.responses.user import UserPaginatedResponse
from core.application.user import UserService
from api.utils.doc_responses import ExceptionResponse
from core.infrastructure.repositories.orm.user import UserAdapter

router = APIRouter()

adapter = UserAdapter()
service = UserService(adapter)


@router.post(
    "",
    response_model=UserResponse,
    responses={
        401: {"model": ExceptionResponse},
        403: {"model": ExceptionResponse},
    },
)
def create_user(
    user_request: UserDTO,
    service: UserService = Depends(lambda: service),
    is_super: bool = Depends(is_super_user),
):
    if not is_super:
        raise HTTPException(status_code=403, detail="Not authorized")

    return service.create_user(user_request)


@router.get(
    "",
    response_model=UserPaginatedResponse,
    responses={
        401: {"model": ExceptionResponse},
        403: {"model": ExceptionResponse},
    },
)
def get_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    service: UserService = Depends(lambda: service),
    is_super: bool = Depends(is_super_user),
):
    if not is_super:
        raise HTTPException(status_code=403, detail="Not authorized")

    return service.get_users(page, page_size)
