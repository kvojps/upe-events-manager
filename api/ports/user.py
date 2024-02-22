from abc import ABC, abstractmethod
from api.models.dto.user import UserDTO

from api.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user_request: User) -> User:
        ...

    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        ...
