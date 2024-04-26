from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from api.config.postgres import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    cpf = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    workload = Column(Float, nullable=True)
    is_present = Column(Boolean, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="subscribers")
