from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api.adapters.repository.user import UserAdapter
from api.models.dto.user import AuthDTO, UserDTO
from api.models.responses.user import AuthResponse, UserResponse
from api.security import is_super_user
from api.services.auth import AuthService

router = APIRouter()

adapter = UserAdapter()
service = AuthService(adapter)


@router.post(
    "/register", 
    responses=
        {201: {"model": UserResponse}, 
         403: {"description": "Not authorized"}},
    response_model=UserResponse
    )
def create_user(
    user_request: UserDTO,
    service: AuthService = Depends(lambda: service),
    is_super: bool = Depends(is_super_user),
):
    if not is_super:
        raise HTTPException(status_code=403, detail="Not authorized")

    return service.create_user(user_request)


@router.post(
    "/login",
    responses=
        {200: {"model": AuthResponse}, 
         401: {"description": "Unauthorized"}},
    response_model=AuthResponse)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(lambda: service),
):
    user_request = AuthDTO(username=form_data.username, password=form_data.password)
    return service.authenticate_user(user_request)
