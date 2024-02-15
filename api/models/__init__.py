from api.config.postgres import engine
from .paper import Paper


def create_tables():
    paper.Base.metadata.create_all(bind=engine)
