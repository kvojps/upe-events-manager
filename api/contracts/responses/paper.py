from typing import Optional
from pydantic import BaseModel
from core.domain.paper import Paper


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


class BatchPapersErrorResponse(BaseModel):
    id: int
    message: str


class BatchPapersResponse(BaseModel):
    detail: str
    errors: list[BatchPapersErrorResponse]


class PapersPaginatedResponse(BaseModel):
    papers: list[PaperResponse]
    total_papers: int
    total_pages: int
    current_page: int

    @classmethod
    def from_papers(
        cls,
        papers: list[Paper],
        total_papers: int,
        total_pages: int,
        current_page: int,
    ) -> "PapersPaginatedResponse":
        return cls(
            papers=[PaperResponse.from_paper(paper) for paper in papers],
            total_papers=total_papers,
            total_pages=total_pages,
            current_page=current_page,
        )


class AreasResponse(BaseModel):
    areas: list[str]
