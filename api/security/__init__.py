from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from api.models.user import UserType
from api.utils.jwt import verify_token

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
