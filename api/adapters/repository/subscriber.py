from api.config.postgres import SessionLocal
from api.models.subscriber import Subscriber
from api.ports.subscriber import SubscriberRepository


class SubscriberAdapter(SubscriberRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_subscriber(self, cpf: str, email: str, event_id: int) -> Subscriber:
        subscriber_data = Subscriber(
            name=None,
            cpf=cpf,
            email=email,
            workload=None,
            is_present=False,
            event_id=event_id,
        )

        self._session.add(subscriber_data)
        self._session.commit()
        self._session.refresh(subscriber_data)

        return subscriber_data
