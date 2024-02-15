from abc import ABC, abstractmethod
from api.models.dto.event import Event as EventDTO
from api.models.event import Event


class EventRepository(ABC):
    @abstractmethod
    def create_event(self, event: EventDTO) -> Event: ...

    @abstractmethod
    def get_events(self) -> list[Event]: ...
