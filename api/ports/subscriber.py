from abc import ABC, abstractmethod
from api.models.dto.subscriber import SubscriberDTO
from api.models.subscriber import Subscriber


class SubscriberRepository(ABC):
    @abstractmethod
    def create_subscriber(self, cpf: str, email: str, event_id: int) -> Subscriber: ...
