from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.adapters.repository.user import UserAdapter
from api.models.user import UserType
from api.services.auth_user import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

adapter = UserAdapter()
service = AuthService(adapter)


def token_verifier(
    token=Depends(oauth2_scheme),
    service: AuthService = Depends(lambda: service),
):
    service.verify_token(token)


def is_super_user(
    token=Depends(oauth2_scheme),
    service: AuthService = Depends(lambda: service),
):
    user = service.verify_token(token)

    return user.user_type == UserType.SUPER.value
