from api.config.postgres import engine, init_postgres_db
from api.utils.create_super_user import create_super_user

from sqlalchemy.ext.declarative import declarative_base
from api.config.postgres import engine, init_postgres_db
from api.utils.create_super_user import create_super_user

Base = declarative_base()

from .event import Event
from .paper import Paper
from .subscriber import Subscriber
from .user import User

__all__ = ["Base", "Event", "Paper", "Subscriber", "User"]

def create_tables():
    Base.metadata.create_all(bind=engine)


def init_config_db():
    create_tables()
    db = next(init_postgres_db())
    create_super_user(db)
