from enum import Enum
from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, String
from api.models.dto.user import UserDTO
from core.infrastructure.settings.db_connection import SqlAlchemyBaseEntity


class UserType(Enum):
    SUPER = "SUPER"
    ADMIN = "ADMIN"


class User(SqlAlchemyBaseEntity):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    user_type = Column(String, nullable=False, default=UserType.ADMIN.value)
    is_active = Column(Boolean, default=True)

    @classmethod
    def from_dto(cls, user_request: UserDTO):
        crypt_context = CryptContext(schemes=["sha256_crypt"])
        return cls(
            username=user_request.email.split("@")[0],
            email=user_request.email,
            password=crypt_context.hash(user_request.password),
        )
