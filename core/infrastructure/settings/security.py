from passlib.context import CryptContext
from api.config.dynaconf import settings
from api.models.user import User, UserType
from core.infrastructure.settings.db_connection import get_session

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
