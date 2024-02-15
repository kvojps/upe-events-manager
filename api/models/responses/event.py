from typing import Optional
from pydantic import BaseModel
from api.models.event import Event


class EventResponse(BaseModel):
    id: int
    name: str
    summary_filename: Optional[str]
    all_papers_filename: Optional[str]
    anal_filename: Optional[str]

    @classmethod
    def from_event(cls, event: Event) -> "EventResponse":
        return cls(
            id=int(event.id),
            name=str(event.name),
            summary_filename=(
                str(event.summary_filename) if event.summary_filename else None
            ),
            all_papers_filename=(
                str(event.all_papers_filename) if event.all_papers_filename else None
            ),
            anal_filename=str(event.anal_filename) if event.anal_filename else None,
        )
