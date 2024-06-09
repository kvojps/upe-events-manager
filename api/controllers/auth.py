from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.models.dto.user import AuthDTO
from api.services.auth import AuthService
from api.services.responses.user import AuthResponse
from core.infrastructure.repositories.orm.user import UserAdapter

router = APIRouter()

adapter = UserAdapter()
service = AuthService(adapter)


@router.post("/login", response_model=AuthResponse)
def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(lambda: service),
):
    user_request = AuthDTO(username=form_data.username, password=form_data.password)
    return service.authenticate_user(user_request)
