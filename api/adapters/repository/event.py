from api.config.postgres import SessionLocal
from api.models.dto.event import EventDTO
from api.models.event import Event
from api.ports.event import EventRepository


class EventAdapter(EventRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_event(self, event: EventDTO) -> Event:
        event_data = Event(
            name=event.name,
            anal_filename=event.anal_filename,
        )

        self._session.add(event_data)
        self._session.commit()
        self._session.refresh(event_data)

        return event_data

    def get_events(self) -> list[Event]:
        return self._session.query(Event).all()
