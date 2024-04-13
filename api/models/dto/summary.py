from pydantic import BaseModel


class SummaryDTO(BaseModel):
    cover_pages_length: int
