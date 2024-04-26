from datetime import datetime
from pydantic import BaseModel
from api.models.user import User


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    @classmethod
    def from_user(cls, user) -> "UserResponse":
        return cls(id=user.id, username=user.username, is_active=user.is_active)


class UserPaginatedResponse(BaseModel):
    users: list[UserResponse]
    total_users: int
    total_pages: int
    current_page: int

    @classmethod
    def from_users(
        cls,
        users: list[User],
        total_users: int,
        total_pages: int,
        current_page: int,
    ) -> "UserPaginatedResponse":
        return cls(
            users=[UserResponse.from_user(user) for user in users],
            total_users=total_users,
            total_pages=total_pages,
            current_page=current_page,
        )


class AuthResponse(BaseModel):
    access_token: str
    expires_in: datetime
    user: UserResponse
