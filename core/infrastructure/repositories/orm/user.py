from api.models.user import User
from core.infrastructure.repositories.user import UserRepository
from core.infrastructure.settings.db_connection import get_session


class UserAdapter(UserRepository):
    def create_user(self, user_request: User) -> User:
        with get_session() as session:
            session.add(user_request)
            session.commit()
            session.refresh(user_request)
            return user_request

    def get_users(self, page: int = 1, page_size: int = 10) -> list[User]:
        with get_session() as session:
            return (
                session.query(User)
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )

    def get_user_by_username(self, username: str) -> User:
        with get_session() as session:
            return session.query(User).filter(User.username == username).first()

    def count_users(self) -> int:
        with get_session() as session:
            return session.query(User).count()
