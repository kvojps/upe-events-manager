from abc import ABC, abstractmethod
from api.models.subscriber import Subscriber


class SubscriberRepository(ABC):
    @abstractmethod
    def create_subscriber(self, cpf: str, email: str, event_id: int) -> Subscriber: ...

    @abstractmethod
    def get_subscribers(
        self,
        event_id: int,
        page: int = 1,
        page_size: int = 10,
    ) -> list[Subscriber]: ...

    @abstractmethod
    def count_subscribers_by_event_id(self, event_id: int) -> int: ...
