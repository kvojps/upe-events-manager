from pydantic import BaseModel
from api.models.paper import Paper


class PaperResponse(BaseModel):
    id: int
    pdf_id: str
    pdf_filename: str
    title: str
    authors: str
    isIgnored: bool
    event_id: int

    @classmethod
    def from_paper(cls, paper: Paper) -> "PaperResponse":
        return cls(
            id=int(paper.id),
            pdf_id=str(paper.pdf_id),
            pdf_filename=str(paper.pdf_filename),
            title=str(paper.title),
            authors=str(paper.authors),
            isIgnored=bool(paper.isIgnored),
            event_id=int(paper.event_id),
        )
