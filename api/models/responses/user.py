from datetime import datetime
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    @classmethod
    def from_user(cls, user) -> "UserResponse":
        return cls(id=user.id, username=user.username, is_active=user.is_active)


class UserLoginResponse(BaseModel):
    access_token: str
    expires_in: datetime
    user: UserResponse
