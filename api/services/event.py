from math import ceil
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel
from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.ports.event import EventRepository
from api.utils.date import str_to_date


class EventsPaginatedResponse(BaseModel):
    events: list[EventResponse]
    total_events: int
    total_pages: int
    current_page: int


class EventService:
    def __init__(
        self,
        event_repo: EventRepository,
    ):
        self._event_repo = event_repo

    def create_event(self, event: EventDTO) -> EventResponse:
        if self._event_repo.get_event_by_name(event.name):
            raise HTTPException(
                status_code=409, detail=f"Event with name {event.name} already exists"
            )

        event_data = self._event_repo.create_event(event)

        return EventResponse.from_event(event_data)

    def get_events(
        self,
        initial_date: Optional[str],
        final_date: Optional[str],
        page: int = 1,
        page_size: int = 10,
    ) -> EventsPaginatedResponse:
        if initial_date:
            str_to_date(initial_date)
        if final_date:
            str_to_date(final_date)

        events_data = self._event_repo.get_events(
            initial_date, final_date, page, page_size
        )
        events_response = [
            EventResponse.from_event(event_data) for event_data in events_data
        ]

        return EventsPaginatedResponse(
            events=events_response,
            total_events=self._event_repo.count_events(initial_date, final_date),
            total_pages=ceil(
                self._event_repo.count_events(initial_date, final_date) / page_size
            ),
            current_page=page,
        )

    def update_summary_filename(
        self, event_id: int, summary_filename: str
    ) -> EventResponse:
        if not self._event_repo.get_event_by_id(event_id):
            raise HTTPException(
                status_code=404, detail=f"Event with id {event_id} not found"
            )

        return EventResponse.from_event(
            self._event_repo.update_summary_filename(event_id, summary_filename)
        )

    def update_merged_papers_filename(
        self, event_id: int, merged_papers_filename: str
    ) -> EventResponse:
        if not self._event_repo.get_event_by_id(event_id):
            raise HTTPException(
                status_code=404, detail=f"Event with id {event_id} not found"
            )

        return EventResponse.from_event(
            self._event_repo.update_merged_papers_filename(
                event_id, merged_papers_filename
            )
        )

    def update_anal_filename(self, event_id: int, anal_filename: str) -> EventResponse:
        if not self._event_repo.get_event_by_id(event_id):
            raise HTTPException(
                status_code=404, detail=f"Event with id {event_id} not found"
            )

        return EventResponse.from_event(
            self._event_repo.update_anal_filename(event_id, anal_filename)
        )
