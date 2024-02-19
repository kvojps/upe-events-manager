from datetime import datetime
from pydantic import BaseModel, validator


class EventDTO(BaseModel):
    name: str
    initial_date: str
    final_date: str

    @validator("initial_date")
    def validate_initial_date(cls, value: str):
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("The initial data must be in the format DD-MM-YYYY")

        return value

    @validator("final_date")
    def validate_final_date(cls, value: str):
        try:
            datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("The initial data must be in the format DD-MM-YYYY")

        return value
