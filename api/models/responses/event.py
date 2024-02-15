from pydantic import BaseModel
from api.models.event import Event


class EventResponse(BaseModel):
    id: int
    name: str
    anal_filename: str

    @classmethod
    def from_event(cls, event: Event) -> "EventResponse":
        return cls(
            id=int(event.id),
            name=str(event.name),
            anal_filename=str(event.anal_filename),
        )
