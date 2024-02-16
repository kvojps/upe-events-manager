from abc import ABC, abstractmethod
from api.models.dto.event import EventDTO
from api.models.event import Event


class EventRepository(ABC):
    @abstractmethod
    def create_event(self, event: EventDTO) -> Event: ...

    @abstractmethod
    def get_events(self, page: int = 1, page_size: int = 10) -> list[Event]: ...

    @abstractmethod
    def get_event_by_id(self, event_id: int) -> Event: ...

    @abstractmethod
    def count_events(self) -> int: ...

    @abstractmethod
    def update_summary_filename(
        self, event_id: int, summary_filename: str
    ) -> Event: ...
