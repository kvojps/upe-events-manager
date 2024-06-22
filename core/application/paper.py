import csv
from math import ceil
from typing import Optional
from fastapi import File, HTTPException, UploadFile, status
from api.contracts.responses.paper import (
    AreasResponse,
    BatchPapersErrorResponse,
    BatchPapersResponse,
    PapersPaginatedResponse,
)
from core.domain.dto.paper import PaperDTO
from core.infrastructure.repositories.event import EventRepository
from core.infrastructure.repositories.paper import PaperRepository


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
                status_code=status.HTTP_400_BAD_REQUEST,
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

        csv_reader = csv.DictReader(decoded_content, delimiter=",")
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
                    area=str(row["area"]).strip(),
                    title=str(row["titulo"]).strip(),
                    authors=row["autores"],
                    is_ignored=False if row["ignorar"] == "n" else True,
                    total_pages=None,
                    event_id=event_id,
                )
            )
        except KeyError as e:
            batch_papers_response.append(
                BatchPapersErrorResponse(
                    id=0,
                    message=f"Error creating subscriber: {str(e)}",
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
        papers_amount = self._paper_repo.count_papers(search, area, event_id)
        return PapersPaginatedResponse.from_papers(
            papers=self._paper_repo.get_papers(search, area, event_id, page, page_size),
            total_papers=papers_amount,
            total_pages=ceil(papers_amount / page_size),
            current_page=page,
        )

    def get_paper_by_id(self, paper_id: int):
        paper = self._paper_repo.get_paper_by_id(paper_id)
        if not paper:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found",
            )

        return paper

    def get_areas(self) -> AreasResponse:
        return AreasResponse(areas=self._paper_repo.get_areas())
