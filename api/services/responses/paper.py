from typing import Optional
from pydantic import BaseModel
from api.models.paper import Paper


class PaperResponse(BaseModel):
    id: int
    pdf_id: str
    area: str
    pdf_filename: str
    title: str
    authors: str
    is_ignored: bool
    total_pages: Optional[int]
    event_id: int

    @classmethod
    def from_paper(cls, paper: Paper) -> "PaperResponse":
        return cls(
            id=int(paper.id),
            pdf_id=str(paper.pdf_id),
            area=str(paper.area),
            pdf_filename=str(paper.pdf_id + ".pdf"),
            title=str(paper.title),
            authors=str(paper.authors),
            is_ignored=bool(paper.is_ignored),
            total_pages=int(paper.total_pages) if paper.total_pages else None,
            event_id=int(paper.event_id),
        )
