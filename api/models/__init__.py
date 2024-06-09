from core.infrastructure.settings.db_connection import engine
from .event import Event
from .paper import Paper
from .subscriber import Subscriber
from .user import User


def create_tables():
    Paper.metadata.create_all(bind=engine)
    Event.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Subscriber.metadata.create_all(bind=engine)
