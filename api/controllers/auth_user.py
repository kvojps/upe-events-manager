from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.adapters.repository.user import UserAdapter
from api.models.dto.user import UserDTO, UserLoginDTO
from api.models.responses.user import UserLoginResponse, UserResponse
from api.security import is_super_user
from api.services.auth_user import AuthService


router = APIRouter()

adapter = UserAdapter()
service = AuthService(adapter)


@router.post("/register", response_model=UserResponse)
def register_user(
    user_request: UserDTO,
    service: AuthService = Depends(lambda: service),
    is_super: bool = Depends(is_super_user),
):
    print(is_super)
    if not is_super:
        raise HTTPException(status_code=403, detail="Not authorized")

    return service.register_user(user_request)


@router.post("/login", response_model=UserLoginResponse)
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(lambda: service),
):
    user_request = UserLoginDTO(
        username=form_data.username, password=form_data.password
    )
    return service.user_login(user_request)
