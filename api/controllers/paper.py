from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from api.adapters.repository.paper import PaperAdapter
from api.models.dto.paper import PaperDTO
from api.models.responses.paper import PaperResponse
from api.services.paper import (
    BatchPapersResponse,
    PaperService,
    PapersPaginatedResponse,
)

router = APIRouter()

adapter = PaperAdapter()
service = PaperService(adapter)


@router.post("", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(
    paper_data: PaperDTO, paper_service: PaperService = Depends(lambda: service)
):
    return paper_service.create_paper(paper_data)


@router.post(
    "/upload_csv/events/{event_id}",
    response_model=list[BatchPapersResponse],
    status_code=status.HTTP_207_MULTI_STATUS,
)
async def batch_create_papers(
    event_id: int,
    file: UploadFile = File(...),
    paper_service: PaperService = Depends(lambda: service),
):
    return await paper_service.batch_create_papers(event_id, file)


@router.get("", response_model=PapersPaginatedResponse, status_code=status.HTTP_200_OK)
def get_papers(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    paper_service: PaperService = Depends(lambda: service),
):
    return paper_service.get_papers(page, page_size)
