from math import ceil
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from api.models.dto.user import UserDTO
from api.models.user import User
from api.ports.user import UserRepository
from api.services.responses.user import UserPaginatedResponse, UserResponse


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repo = user_repository

    def create_user(self, user: UserDTO) -> UserResponse:
        user_data = User.from_dto(user)

        try:
            return UserResponse.from_user(self._user_repo.create_user(user_data))
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists")

    def get_users(self, page: int = 1, per_page: int = 10) -> UserPaginatedResponse:
        users_amount = self._user_repo.count_users()
        return UserPaginatedResponse.from_users(
            users=self._user_repo.get_users(page, per_page),
            total_users=users_amount,
            total_pages=ceil(users_amount / per_page),
            current_page=page,
        )