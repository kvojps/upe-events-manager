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
            initial_date=event.initial_date,
            final_date=event.final_date,
            s3_folder_name=f"""{event.name.lower().replace(" ", "_")}__{str(uuid.uuid4())}__{event.initial_date}_{event.final_date}""",
            summary_filename=None,
            merged_papers_filename=None,
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

    def get_event_by_id(self, event_id: int) -> Event:
        return self._session.query(Event).filter(Event.id == event_id).first()

    def count_events(self) -> int:
        return self._session.query(Event).count()

    def update_summary_filename(self, event_id: int, summary_filename: str) -> Event:
        event = self.get_event_by_id(event_id)
        event.summary_filename = summary_filename  # type: ignore
        self._session.commit()
        self._session.refresh(event)

        return event

    def update_merged_papers_filename(
        self, event_id: int, merged_papers_filename: str
    ) -> Event:
        event = self.get_event_by_id(event_id)
        event.merged_papers_filename = merged_papers_filename  # type: ignore
        self._session.commit()
        self._session.refresh(event)

        return event
