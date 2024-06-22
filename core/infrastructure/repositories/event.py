from abc import ABC, abstractmethod
from typing import Optional
from api.models.dto.event import EventDTO
from core.domain.event import Event


class EventRepository(ABC):
    @abstractmethod
    def create_event(self, event: EventDTO) -> Event: ...

    @abstractmethod
    def get_events(
        self,
        initial_date: Optional[str],
        final_date: Optional[str],
        name: Optional[str],
        page: int = 1,
        page_size: int = 10,
    ) -> list[Event]: ...

    @abstractmethod
    def get_event_by_id(self, event_id: int) -> Event: ...

    @abstractmethod
    def get_event_by_name(self, event_name: str) -> Event: ...

    @abstractmethod
    def count_events(
        self,
        initial_date: Optional[str],
        final_date: Optional[str],
        name: Optional[str],
    ) -> int: ...

    @abstractmethod
    def update_summary_filename(
        self, event_id: int, summary_filename: str
    ) -> Event: ...

    @abstractmethod
    def update_merged_papers_filename(
        self, event_id: int, merged_papers_filename: str
    ) -> Event: ...

    @abstractmethod
    def update_anal_filename(self, event_id: int, anal_filename: str) -> Event: ...
