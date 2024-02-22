from fastapi import HTTPException
from jose import JWTError, jwt
from api.adapters.repository.user import UserAdapter
from api.config.dynaconf import settings


def _get_user_adapter():
    return UserAdapter()


# TODO: Use dependency injection
user_adapter = _get_user_adapter()


async def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_data = user_adapter.get_user_by_username(payload["sub"])

    if user_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_data
