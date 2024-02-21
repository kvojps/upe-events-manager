from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.config.postgres import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(String, unique=True, index=True)
    area = Column(String)
    title = Column(String)
    authors = Column(String)
    is_ignored = Column(Boolean)
    total_pages = Column(Integer)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="papers")
