from abc import ABC, abstractmethod
from typing import Optional
from core.domain.subscriber import Subscriber


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
    def get_listeners(self, event_id: int) -> list[Subscriber]: ...

    @abstractmethod
    def get_event_subscriber_by_email(
        self, event_id: int, email: str
    ) -> Optional[Subscriber]: ...

    @abstractmethod
    def count_subscribers_by_event_id(self, event_id: int) -> int: ...

    @abstractmethod
    def update_subscriber(self, subscriber: Subscriber) -> Subscriber: ...
