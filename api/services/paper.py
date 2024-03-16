import csv
from math import ceil
from typing import List, Union, Optional

from fastapi import File, HTTPException, UploadFile, status
from pydantic import BaseModel
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
    ) -> Union[List[BatchPapersResponse], BatchPapersResponse]:
        event = self._event_repo.get_event_by_id(event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found",
            )

        if not event.merged_papers_filename:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Merged papers file not found",
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

        errors: List[BatchPapersResponse] = []
        success_message = "All papers updated successfully"
        for row in csv_reader:
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
                errors.append(
                    BatchPapersResponse(
                        id=int(row.get("id", 0)),
                        message=f"Error updating paper: {str(e)}",
                    )
                )

        if errors:
            return errors
        else:
            return [BatchPapersResponse(id=0, message=success_message)]

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
