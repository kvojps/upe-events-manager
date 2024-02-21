from pydantic import BaseModel


class PaperDTO(BaseModel):
    pdf_id: str
    area: str
    title: str
    authors: str
    is_ignored: bool
    total_pages: int
    event_id: int
