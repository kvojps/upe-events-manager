from pydantic import BaseModel


class EventResponse(BaseModel):
    name: str
    anal_filename: str
