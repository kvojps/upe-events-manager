from typing import Optional
from pydantic import BaseModel
from core.domain.event import Event
from core.domain.paper import Paper
from core.infrastructure.settings.db_connection import get_session
from core.infrastructure.settings.env_handler import settings


class PaperResponse(BaseModel):
    id: int
    pdf_id: str
    area: str
    pdf_filename: str
    title: str
    authors: str
    is_ignored: bool
    total_pages: Optional[int]
    pdf_download_link: str
    event_id: int
    event_name: str

    @classmethod
    def from_paper(cls, paper: Paper) -> "PaperResponse":
        #TODO: REFACTOR THIS TO LAZY LOAD THE EVENT
        with get_session() as session:
            event = session.get(Event, paper.event_id)

            return cls(
                id=int(paper.id),
                pdf_id=str(paper.pdf_id),
                area=str(paper.area),
                pdf_filename=str(paper.pdf_id + ".pdf"),
                title=str(paper.title),
                authors=str(paper.authors),
                is_ignored=bool(paper.is_ignored),
                total_pages=int(paper.total_pages) if paper.total_pages else None,
                pdf_download_link=settings.S3_BASE_URL
                + f"{str(event.s3_folder_name)}/"
                + str(paper.pdf_id + ".pdf"),
                event_id=int(paper.event_id),
                event_name=str(event.name),
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
