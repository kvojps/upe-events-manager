from abc import ABC, abstractmethod
from core.domain.subscriber import Subscriber


class EmailHandlerProvider(ABC):
    @abstractmethod
    def send_raw_email(self, file: bytes, listener: Subscriber) -> None: ...
