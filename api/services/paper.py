import csv
from math import ceil
from fastapi import File, HTTPException, UploadFile, status
from pydantic import BaseModel
from api.models.dto.paper import PaperDTO
from api.models.responses.paper import PaperResponse
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
    def __init__(self, paper_repo: PaperRepository):
        self._paper_repo = paper_repo

    async def batch_create_papers(
        self, event_id: int, file: UploadFile = File(...)
    ) -> list[BatchPapersResponse]:
        if not file.filename or not file.filename.endswith(".csv"):
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail="Only CSV files are allowed",
            )

        if self._paper_repo.count_papers_by_event_id(event_id) > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Papers already created for this event",
            )

        contents = await file.read()
        decoded_content = contents.decode("utf-8").splitlines()
        csv_reader = csv.DictReader(decoded_content, delimiter=";")

        batch_papers: list[BatchPapersResponse] = []
        for row in csv_reader:
            try:
                self._paper_repo.create_paper(
                    PaperDTO(
                        pdf_id=row["id"],
                        area=row["area"],
                        title=row["titulo"],
                        authors=row["autores"],
                        isIgnored=False if row["ignorar"] == "n" else True,
                        event_id=event_id,
                    )
                )

                batch_papers.append(
                    BatchPapersResponse(
                        id=int(row["id"]),
                        message="Paper created successfully",
                    )
                )
            except Exception as e:
                batch_papers.append(
                    BatchPapersResponse(
                        id=int(row["id"]),
                        message=f"Error creating paper: {str(e)}",
                    )
                )

        return batch_papers

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
