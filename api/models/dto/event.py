from pydantic import BaseModel


class EventDTO(BaseModel):
    name: str
    anal_filename: str
