from api.config.postgres import engine, init_postgres_db
from api.utils.create_super_user import create_super_user
from .paper import Paper
from .event import Event
from .user import User


def create_tables():
    paper.Base.metadata.create_all(bind=engine)
    event.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)


def init_config_db():
    create_tables()
    db = next(init_postgres_db())
    create_super_user(db)
