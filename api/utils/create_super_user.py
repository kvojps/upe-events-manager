from api.config.dynaconf import settings
from passlib.context import CryptContext

from api.models.user import User, UserType

crypt_context = CryptContext(schemes=["sha256_crypt"])


def create_super_user(session):
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
        print(f"Super user {settings.SUPER_USER_EMAIL} created successfully.")
    else:
        print("Super user already exists.")
