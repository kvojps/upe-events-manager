from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from api.contracts.responses.user import AuthResponse, UserResponse
from api.models.dto.user import AuthDTO
from core.infrastructure.repositories.user import UserRepository
from core.infrastructure.settings.env_handler import settings

CRYPT_CONTEXT = CryptContext(schemes=["sha256_crypt"])


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
        self._jwt_secret_key = settings.JWT_SECRET_KEY
        self._jwt_algorithm = settings.JWT_ALGORITHM

    def authenticate_user(self, auth: AuthDTO) -> AuthResponse:
        user_data = self._user_repo.get_user_by_username(auth.username)

        if user_data is None:
            raise HTTPException(
                status_code=401, detail="Username or password incorrect"
            )

        if not CRYPT_CONTEXT.verify(auth.password, str(user_data.password)):
            raise HTTPException(
                status_code=401, detail="Username or password incorrect"
            )

        expiration_time = datetime.utcnow() + timedelta(days=1)

        payload = {"sub": user_data.username, "exp": expiration_time}

        access_token = jwt.encode(
            payload, self._jwt_secret_key, algorithm=self._jwt_algorithm
        )

        return AuthResponse(
            access_token=access_token,
            expires_in=expiration_time,
            user=UserResponse.from_user(user_data),
        )
