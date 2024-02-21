from typing import Optional
from pydantic import BaseModel


class PaperDTO(BaseModel):
    pdf_id: str
    area: Optional[str]
    title: Optional[str]
    authors: Optional[str]
    is_ignored: Optional[bool]
    total_pages: int
    event_id: Optional[int]
