from pydantic import BaseModel


class Event(BaseModel):
    name: str
    anal_filename: str
