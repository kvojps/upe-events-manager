from datetime import datetime
from math import ceil
from typing import Optional
from fastapi import HTTPException, status
from api.contracts.responses.event import EventResponse, EventsPaginatedResponse
from core.domain.dto.event import EventDTO
from core.infrastructure.repositories.event import EventRepository


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
        name: Optional[str],
        page: int = 1,
        page_size: int = 10,
        sort_by: str = 'initial_date',
        sort_direction: str = 'asc',
    ) -> EventsPaginatedResponse:
        if initial_date:
            self._str_to_date(initial_date)
        if final_date:
            self._str_to_date(final_date)

        events_amount = self._event_repo.count_events(initial_date, final_date, name)
        return EventsPaginatedResponse.from_events(
            events=self._event_repo.get_events(
                initial_date, final_date, name, page, page_size, sort_by, sort_direction
            ),
            total_events=events_amount,
            total_pages=ceil(events_amount / page_size),
            current_page=page,
        )

    def get_event_by_id(self, event_id: int) -> EventResponse:
        event = self._event_repo.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail=f"Event not found")

        return EventResponse.from_event(event)

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

    def _str_to_date(self, date: str) -> datetime:
        try:
            return datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Date format should be DD-MM-YYYY",
            )
