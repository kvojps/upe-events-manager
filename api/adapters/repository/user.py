from api.config.postgres import SessionLocal
from api.models.dto.user import UserDTO
from api.models.user import User
from api.ports.user import UserRepository


class UserAdapter(UserRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_user(self, user_request: User) -> User:
        self._session.add(user_request)
        self._session.commit()
        self._session.refresh(user_request)
        return user_request

    def get_users(self, page: int = 1, page_size: int = 10) -> list[User]:
        return (
            self._session.query(User)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

    def get_user_by_username(self, username: str) -> User:
        return self._session.query(User).filter(User.username == username).first()

    def count_users(self) -> int:
        return self._session.query(User).count()
