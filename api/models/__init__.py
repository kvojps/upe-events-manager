from api.config.postgres import engine
from .paper import Paper
from .event import Event


def create_tables():
    paper.Base.metadata.create_all(bind=engine)
    event.Base.metadata.create_all(bind=engine)
