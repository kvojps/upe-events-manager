from pydantic import BaseModel
from api.models.paper import Paper


class PaperResponse(BaseModel):
    pdf_id: str
    pdf_filename: str
    email: str
    title: str
    authors: str
    isIgnored: bool
    event_id: int

    @classmethod
    def from_paper(cls, paper: Paper) -> "PaperResponse":
        return cls(
            pdf_id=str(paper.pdf_id),
            pdf_filename=str(paper.pdf_filename),
            email=str(paper.email),
            title=str(paper.title),
            authors=str(paper.authors),
            isIgnored=bool(paper.isIgnored),
            event_id=int(paper.event_id),
        )
