from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from core.infrastructure.settings.db_connection import SqlAlchemyBaseEntity


class Paper(SqlAlchemyBaseEntity):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(String, index=True)
    area = Column(String)
    title = Column(String)
    authors = Column(String)
    is_ignored = Column(Boolean)
    total_pages = Column(Integer)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="papers")
