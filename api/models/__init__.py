from api.config.postgres import engine
from .paper import Paper
from .event import Event
from .user import User


def create_tables():
    paper.Base.metadata.create_all(bind=engine)
    event.Base.metadata.create_all(bind=engine)
    user.Base.metadata.create_all(bind=engine)
