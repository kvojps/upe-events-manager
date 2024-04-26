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

    def get_subscribers(
        self,
        event_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Subscriber]:
        return (
            self._session.query(Subscriber)
            .filter(Subscriber.event_id == event_id)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

    def count_subscribers_by_event_id(self, event_id: int) -> int:
        return (
            self._session.query(Subscriber)
            .filter(Subscriber.event_id == event_id)
            .count()
        )
