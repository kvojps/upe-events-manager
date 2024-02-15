from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.config.postgres import Base


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(String, unique=True, index=True)
    pdf_filename = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    title = Column(String)
    authors = Column(String)
    isIgnored = Column(Boolean, default=False)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="papers")
