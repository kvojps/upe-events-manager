import csv
from math import ceil
from typing import Optional
from fastapi import File, HTTPException, UploadFile, status
from pydantic import BaseModel
from api.models.dto.paper import PaperToUpdateDTO
from api.models.responses.paper import PaperResponse
from api.ports.event import EventRepository
from api.ports.paper import PaperRepository


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


class PaperService:
    def __init__(self, paper_repo: PaperRepository, event_repo: EventRepository):
        self._paper_repo = paper_repo
        self._event_repo = event_repo

    async def batch_update_papers(
        self, event_id: int, file: UploadFile = File(...)
    ) -> BatchPapersResponse:
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

        batch_papers_errors: list[BatchPapersErrorResponse] = []
        for row in csv_reader:
            self._update_paper_by_csv_row(row, batch_papers_errors)

        return BatchPapersResponse(
            detail="Batch papers finished", errors=batch_papers_errors
        )

    def _update_paper_by_csv_row(
        self, row, batch_papers_response: list[BatchPapersErrorResponse]
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
        except Exception as e:
            batch_papers_response.append(
                BatchPapersErrorResponse(
                    id=int(row["id"]),
                    message=f"Error creating paper: {str(e)}",
                )
            )

    def get_papers(
        self, search: Optional[str], page: int = 1, page_size: int = 10
    ) -> PapersPaginatedResponse:
        papers_data = self._paper_repo.get_papers(search, page, page_size)
        papers_response = [
            PaperResponse.from_paper(paper_data) for paper_data in papers_data
        ]

        return PapersPaginatedResponse(
            papers=papers_response,
            total_papers=self._paper_repo.count_papers(search),
            total_pages=ceil(self._paper_repo.count_papers(search) / page_size),
            current_page=page,
        )
