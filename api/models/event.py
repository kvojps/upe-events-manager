from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.config.postgres import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    initial_date = Column(String)
    final_date = Column(String)
    s3_folder_name = Column(String)
    summary_filename = Column(String)
    all_papers_filename = Column(String)
    anal_filename = Column(String)

    papers = relationship("Paper", back_populates="event")
