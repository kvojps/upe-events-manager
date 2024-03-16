import csv
from math import ceil
from typing import Optional, List

from fastapi import File, HTTPException, UploadFile, status
from pydantic import BaseModel

from api.models import Paper
from api.models.dto.paper import PaperToUpdateDTO
from api.models.responses.paper import PaperResponse
from api.ports.event import EventRepository
from api.ports.paper import PaperRepository


class BatchPapersResponse(BaseModel):
    id: int
    message: str


class PapersPaginatedResponse(BaseModel):
    papers: list[PaperResponse]
    total_papers: int
    total_pages: int
    current_page: int


class PaperService:
    def __init__(self, paper_repo: PaperRepository, event_repo: EventRepository):
        self._paper_repo = paper_repo
        self._event_repo = event_repo

    async def batch_update_papers(
        self, event_id: int, file: UploadFile = File(...)
    ) -> list[BatchPapersResponse]:
        event = self._event_repo.get_event_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if not event.merged_papers_filename:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merged paprs file not found",
            )

        if self._paper_repo.count_papers_by_event_id(event_id) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Papers not found for this event",
            )

        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only CSV files are allowed",
            )

        contents = await file.read()
        decoded_content = contents.decode("utf-8").splitlines()
        csv_reader = csv.DictReader(decoded_content, delimiter=";")

        batch_papers: list[BatchPapersResponse] = []
        for row in csv_reader:
            self._update_paper_by_csv_row(row, batch_papers)

        return batch_papers

    def _update_paper_by_csv_row(
        self, row, batch_papers_response: list[BatchPapersResponse]
    ) -> None:
        try:
            self._paper_repo.update_paper(
                row["id"],
                PaperToUpdateDTO(
                    area=row["area"],
                    title=row["titulo"],
                    authors=row["autores"],
                    is_ignored=False if row["ignorar"] == "n" else True,
                ),
            )

            batch_papers_response.append(
                BatchPapersResponse(
                    id=int(row["id"]),
                    message="Paper updated successfully",
                )
            )
        except Exception as e:
            batch_papers_response.append(
                BatchPapersResponse(
                    id=int(row["id"]),
                    message=f"Error creating paper: {str(e)}",
                )
            )

    def get_papers(self, page: int = 1, page_size: int = 10) -> PapersPaginatedResponse:
        papers_data = self._paper_repo.get_papers(page, page_size)
        papers_response = [
            PaperResponse.from_paper(paper_data) for paper_data in papers_data
        ]

        return PapersPaginatedResponse(
            papers=papers_response,
            total_papers=self._paper_repo.count_papers(),
            total_pages=ceil(self._paper_repo.count_papers() / page_size),
            current_page=page,
        )

    def get_not_ignored_papers(self) -> List[Paper]:
        not_ignored_papers = self._paper_repo.get_not_ignored_papers()
        if not not_ignored_papers:
            raise HTTPException(status_code=404, detail=" No -not ignored papers- found")

        return not_ignored_papers

    def filter_papers_by_criteria(
            self,
            title: Optional[str] = None,
            author: Optional[str] = None,
            pdf_id: Optional[str] = None,
            area: Optional[str] = None,
            event_id: Optional[int] = None,
    ) -> List[Paper]:
        return self._paper_repo.filter_papers_by_criteria(
            title=title, author=author, pdf_id=pdf_id, area=area, event_id=event_id
        )
