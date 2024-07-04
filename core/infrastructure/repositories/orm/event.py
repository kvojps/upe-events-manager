import uuid
from typing import Optional
from core.domain.dto.event import EventDTO
from core.domain.event import Event
from core.infrastructure.repositories.event import EventRepository
from core.infrastructure.settings.db_connection import get_session
from sqlalchemy import asc, desc, func


class EventAdapter(EventRepository):
    def create_event(self, event: EventDTO) -> Event:
        with get_session() as session:
            event_data = Event(
                name=event.name,
                initial_date=event.initial_date,
                final_date=event.final_date,
                promoted_by=event.promoted_by,
                s3_folder_name=f"""{event.name.lower().replace(" ", "_")}__{str(uuid.uuid4())}__{event.initial_date}_{event.final_date}""",
                summary_filename=None,
                merged_papers_filename=None,
            )

            session.add(event_data)
            session.commit()
            session.refresh(event_data)

            return event_data

    def get_events(
        self,
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = 'initial_date',
        sort_direction: str = 'asc'
    ) -> list[Event]:
        with get_session() as session:
            query = session.query(Event)
            #Valid Sort By
            valid_sort_fields = {"id",
                "name",
                "initial_date",
                "final_date",
                "promoted_by"
            }
            #Change invalid fields
            if sort_by not in valid_sort_fields:
                sort_by = "name"
            
            if sort_direction not in {"asc", "desc"}:
                sort_direction = "asc"
            
            if initial_date:
                query = query.filter(Event.initial_date >= initial_date)
            if final_date:
                query = query.filter(Event.final_date <= final_date)
            if name:
                query = query.filter(Event.name.ilike(f"%{name}%"))
            
            # Apply sorting
            if sort_by:
                sort_column = getattr(Event, sort_by, None)
                if sort_column:
                    if sort_direction == 'asc':
                        if sort_by == 'initial_date' or sort_by == 'final_date':
                            query = query.order_by(func.to_date(sort_column, 'DD-MM-YY').asc())
                        else:
                            query = query.order_by(asc(sort_column))
                    else:
                        if sort_by == 'initial_date' or sort_by == 'final_date':
                            query = query.order_by(func.to_date(sort_column, 'DD-MM-YY').desc())
                        else:
                            query = query.order_by(desc(sort_column))

            # Apply pagination
            query = query.limit(page_size).offset((page - 1) * page_size)
            
            return query.all()

    def get_event_by_id(self, event_id: int) -> Event:
        with get_session() as session:
            return session.query(Event).filter(Event.id == event_id).first()

    def get_event_by_name(self, event_name: str) -> Event:
        with get_session() as session:
            return session.query(Event).filter(Event.name == event_name).first()

    def count_events(
        self,
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
        name: Optional[str] = None,
    ) -> int:
        with get_session() as session:
            return (
                session.query(Event)
                .filter(
                    Event.initial_date >= initial_date if initial_date else True,
                    Event.final_date <= final_date if final_date else True,
                    Event.name.like(f"%{name}%") if name else True,
                )
                .count()
            )

    def update_summary_filename(self, event_id: int, summary_filename: str) -> Event:
        with get_session() as session:
            event = self.get_event_by_id(event_id)
            event.summary_filename = summary_filename  # type: ignore
            session.commit()
            session.refresh(event)

            return event

    def update_merged_papers_filename(
        self, event_id: int, merged_papers_filename: str
    ) -> Event:
        with get_session() as session:
            event = self.get_event_by_id(event_id)
            event.merged_papers_filename = merged_papers_filename  # type: ignore
            session.commit()
            session.refresh(event)

            return event

    def update_anal_filename(self, event_id: int, anal_filename: str) -> Event:
        with get_session() as session:
            event = self.get_event_by_id(event_id)
            event.anal_filename = anal_filename  # type: ignore
            session.commit()
            session.refresh(event)

            return event
