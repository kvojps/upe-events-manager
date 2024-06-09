from typing import Optional
from pydantic import BaseModel
from core.infrastructure.settings.env_handler import settings
from api.models.event import Event


class EventResponse(BaseModel):
    id: int
    name: str
    initial_date: str
    final_date: str
    promoted_by: str
    s3_folder_name: str
    summary_filename: Optional[str]
    merged_papers_filename: Optional[str]
    anal_filename: Optional[str]

    @classmethod
    def from_event(cls, event: Event) -> "EventResponse":
        return cls(
            id=int(event.id),
            name=str(event.name),
            initial_date=str(event.initial_date),
            final_date=str(event.final_date),
            promoted_by=str(event.promoted_by),
            s3_folder_name=str(event.s3_folder_name),
            summary_filename=(
                settings.S3_BASE_URL + str(event.summary_filename)
                if event.summary_filename
                else None
            ),
            merged_papers_filename=(
                settings.S3_BASE_URL + str(event.merged_papers_filename)
                if event.merged_papers_filename
                else None
            ),
            anal_filename=(
                settings.S3_BASE_URL + str(event.anal_filename)
                if event.anal_filename
                else None
            ),
        )


class EventsPaginatedResponse(BaseModel):
    events: list[EventResponse]
    total_events: int
    total_pages: int
    current_page: int

    @classmethod
    def from_events(
        cls, events: list[Event], total_events: int, total_pages: int, current_page: int
    ) -> "EventsPaginatedResponse":
        return cls(
            events=[EventResponse.from_event(event) for event in events],
            total_events=total_events,
            total_pages=total_pages,
            current_page=current_page,
        )
