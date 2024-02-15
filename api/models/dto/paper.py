from pydantic import BaseModel


class PaperDTO(BaseModel):
    pdf_id: str
    pdf_filename: str
    title: str
    authors: str
    isIgnored: bool
    event_id: int
