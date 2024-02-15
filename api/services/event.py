from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.ports.event import EventRepository


class EventService:
    def __init__(self, event_repo: EventRepository):
        self._event_repo = event_repo

    def create_event(self, event: EventDTO) -> EventResponse:
        event_data = self._event_repo.create_event(event)

        return EventResponse(
            name=str(event_data.name), anal_filename=str(event_data.anal_filename)
        )

    def get_events(self) -> list[EventResponse]:
        events_data = self._event_repo.get_events()

        return [
            EventResponse(name=str(event.name), anal_filename=str(event.anal_filename))
            for event in events_data
        ]
