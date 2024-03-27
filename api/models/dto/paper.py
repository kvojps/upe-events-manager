from typing import Optional
from pydantic import BaseModel


class PaperDTO(BaseModel):
    pdf_id: str
    area: str
    title: str
    authors: str
    is_ignored: bool
    total_pages: Optional[int]
    event_id: int
