import uuid
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
            s3_folder_name=event.name.lower().replace(" ", "_")
            + "__"
            + str(uuid.uuid4()),
            summary_filename=None,
            all_papers_filename=None,
        )

        self._session.add(event_data)
        self._session.commit()
        self._session.refresh(event_data)

        return event_data

    def get_events(self, page: int = 1, page_size: int = 10) -> list[Event]:
        return (
            self._session.query(Event)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

    def count_events(self) -> int:
        return self._session.query(Event).count()
