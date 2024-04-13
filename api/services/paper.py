import csv
from math import ceil
from typing import Optional
from fastapi import File, HTTPException, UploadFile, status
from api.models.dto.paper import PaperDTO
from api.ports.event import EventRepository
from api.ports.paper import PaperRepository
from api.services.responses.paper import (
    BatchPapersErrorResponse,
    BatchPapersResponse,
    PapersPaginatedResponse,
    AreasResponse,
)


class PaperService:
    def __init__(self, paper_repo: PaperRepository, event_repo: EventRepository):
        self._paper_repo = paper_repo
        self._event_repo = event_repo

    async def batch_create_papers(
        self, event_id: int, file: UploadFile = File(...)
    ) -> BatchPapersResponse:
        event = self._event_repo.get_event_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if self._paper_repo.count_papers_by_event_id(event_id) > 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Papers already created for this event",
            )

        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only CSV files are allowed",
            )

        content = await file.read()
        try:
            decoded_content = content.decode("utf-8").splitlines()
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Invalid CSV file: Format must be utf-8",
            )

        csv_reader = csv.DictReader(decoded_content, delimiter=";")
        batch_papers_errors: list[BatchPapersErrorResponse] = []
        for row in csv_reader:
            self._create_paper_by_csv_row(row, int(event.id), batch_papers_errors)

        return BatchPapersResponse(
            detail="Batch papers finished", errors=batch_papers_errors
        )

    def _create_paper_by_csv_row(
        self, row, event_id: int, batch_papers_response: list[BatchPapersErrorResponse]
    ) -> None:
        try:
            self._paper_repo.create_paper(
                PaperDTO(
                    pdf_id=row["id"],
                    area=row["area"],
                    title=row["titulo"],
                    authors=row["autores"],
                    is_ignored=False if row["ignorar"] == "n" else True,
                    total_pages=None,
                    event_id=event_id,
                )
            )
        except Exception as e:
            batch_papers_response.append(
                BatchPapersErrorResponse(
                    id=int(row["id"]),
                    message=f"Error creating paper: {str(e)}",
                )
            )

    def get_papers(
        self,
        search: Optional[str],
        area: Optional[str],
        event_id: Optional[int],
        page: int = 1,
        page_size: int = 10,
    ) -> PapersPaginatedResponse:
        return PapersPaginatedResponse.from_papers(
            papers=self._paper_repo.get_papers(search, area, event_id, page, page_size),
            total_papers=self._paper_repo.count_papers(search, area, event_id),
            total_pages=ceil(
                self._paper_repo.count_papers(search, area, event_id) / page_size
            ),
            current_page=page,
        )

    def get_areas(self) -> AreasResponse:
        return AreasResponse(areas=self._paper_repo.get_areas())
