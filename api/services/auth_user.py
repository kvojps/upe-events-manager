from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.config.dynaconf import settings
from api.models.dto.user import UserDTO, UserLoginDTO
from api.models.responses.user import UserResponse, UserLoginResponse
from api.models.user import User
from api.ports.user import UserRepository

crypt_context = CryptContext(schemes=["sha256_crypt"])


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
        self._JWT_SECRET_KEY = settings.JWT_SECRET_KEY
        self._JWT_ALGORITHM = settings.JWT_ALGORITHM

    def register_user(self, user_request: UserDTO) -> UserResponse:
        user = User.from_dto(user_request)

        try:
            user_created = self._user_repo.create_user(user)
            return UserResponse.from_user(user_created)

        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")

    def user_login(self, user_request: UserLoginDTO) -> UserLoginResponse:
        user_db = self._user_repo.get_user_by_username(user_request.username)

        if user_db is None:
            raise HTTPException(
                status_code=401, detail="Username or password incorrect"
            )

        if not crypt_context.verify(user_request.password, user_db.password):  # type: ignore
            raise HTTPException(
                status_code=401, detail="Username or password incorrect"
            )

        exp = datetime.utcnow() + timedelta(minutes=(30))

        payload = {"sub": user_db.username, "exp": exp}

        access_token = jwt.encode(
            payload, self._JWT_SECRET_KEY, algorithm=self._JWT_ALGORITHM
        )

        return UserLoginResponse(
            access_token=access_token,
            expires_in=exp,
            user=UserResponse.from_user(user_db),
        )

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(
                token, self._JWT_SECRET_KEY, algorithms=[self._JWT_ALGORITHM]
            )

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_db = self._user_repo.get_user_by_username(payload["sub"])

        if user_db is None:
            raise HTTPException(status_code=401, detail="Invalid token")
