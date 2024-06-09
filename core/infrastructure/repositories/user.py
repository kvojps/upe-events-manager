from abc import ABC, abstractmethod

from api.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user_request: User) -> User: ...

    @abstractmethod
    def get_users(self, page: int = 1, page_size: int = 10) -> list[User]: ...

    @abstractmethod
    def get_user_by_username(self, username: str) -> User: ...

    @abstractmethod
    def count_users(self) -> int: ...
