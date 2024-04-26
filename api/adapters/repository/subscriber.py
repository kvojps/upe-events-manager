from api.config.postgres import SessionLocal
from api.models.dto.subscriber import SubscriberDTO
from api.models.subscriber import Subscriber
from api.ports.subscriber import SubscriberRepository


class SubscriberAdapter(SubscriberRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_subscriber(self, subscriber: SubscriberDTO) -> Subscriber:
        subscriber_data = Subscriber(
            name=subscriber.name,
            cpf=subscriber.cpf,
            email=subscriber.email,
            workload=subscriber.workload,
            is_present=False,
            event_id=subscriber.event_id,
        )

        self._session.add(subscriber_data)
        self._session.commit()
        self._session.refresh(subscriber_data)

        return subscriber_data
