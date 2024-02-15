from pydantic import BaseModel


class EventDTO(BaseModel):
    name: str
