from pydantic import BaseModel
from api.models.event import Event


class EventResponse(BaseModel):
    name: str
    anal_filename: str

    @classmethod
    def from_event(cls, event: Event) -> "EventResponse":
        return cls(name=str(event.name), anal_filename=str(event.anal_filename))
