from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.adapters.repository.user import UserAdapter
from api.ports.user import UserRepository
from api.services.auth_user import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/aut/login")

adapter = UserAdapter()
service = AuthService(adapter)


def token_verifier(
    adapter: UserRepository = Depends(lambda: adapter),
    token=Depends(oauth2_scheme),
    service: AuthService = Depends(lambda: service),
):
    service.verify_token(token)
