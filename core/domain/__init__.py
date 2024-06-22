from core.domain.event import Event
from core.domain.subscriber import Subscriber
from core.domain.user import User
from core.domain.paper import Paper
from core.infrastructure.settings.db_connection import engine


def create_tables():
    Paper.metadata.create_all(bind=engine)
    Event.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)
    Subscriber.metadata.create_all(bind=engine)
