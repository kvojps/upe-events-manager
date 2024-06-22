from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from core.domain.user import UserType
from api.utils.jwt import verify_token
from core.domain.user import User
from core.infrastructure.settings.db_connection import get_session
from core.infrastructure.settings.env_handler import settings

crypt_context = CryptContext(schemes=["sha256_crypt"])


def create_super_user():
    with get_session() as session:
        super_user = (
            session.query(User).filter(User.email == settings.SUPER_USER_EMAIL).first()
        )

        if super_user is None:
            super_user = User(
                username=settings.SUPER_USER_EMAIL.split("@")[0],
                email=settings.SUPER_USER_EMAIL,
                password=crypt_context.hash(settings.SUPER_USER_PASSWORD),
                user_type=UserType.SUPER.value,
            )
            session.add(super_user)
            session.commit()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def is_valid_token(
    token=Depends(oauth2_scheme),
):
    await verify_token(token)


async def is_super_user(
    token=Depends(oauth2_scheme),
):
    user = await verify_token(token)

    return user.user_type == UserType.SUPER.value
