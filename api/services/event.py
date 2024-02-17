from math import ceil
from pydantic import BaseModel
from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.ports.event import EventRepository


class EventsPaginatedResponse(BaseModel):
    events: list[EventResponse]
    total_papers: int
    total_pages: int
    current_page: int


class EventService:
    def __init__(
        self,
        event_repo: EventRepository,
    ):
        self._event_repo = event_repo

    def create_event(self, event: EventDTO) -> EventResponse:
        event_data = self._event_repo.create_event(event)

        return EventResponse.from_event(event_data)

    def get_events(self, page: int = 1, page_size: int = 10) -> EventsPaginatedResponse:
        events_data = self._event_repo.get_events(page, page_size)
        events_response = [
            EventResponse.from_event(event_data) for event_data in events_data
        ]

        return EventsPaginatedResponse(
            events=events_response,
            total_papers=self._event_repo.count_events(),
            total_pages=ceil(self._event_repo.count_events() / page_size),
            current_page=page,
        )

    def update_summary_filename(
        self, event_id: int, summary_filename: str
    ) -> EventResponse:
        return EventResponse.from_event(
            self._event_repo.update_summary_filename(event_id, summary_filename)
        )

    def update_merged_papers_filename(
        self, event_id: int, merged_papers_filename: str
    ) -> EventResponse:
        return EventResponse.from_event(
            self._event_repo.update_merged_papers_filename(
                event_id, merged_papers_filename
            )
        )
