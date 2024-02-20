from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from api.adapters.repository.paper import PaperAdapter
from api.services.paper import (
    BatchPapersResponse,
    PaperService,
    PapersPaginatedResponse,
)

router = APIRouter()

adapter = PaperAdapter()
service = PaperService(adapter)


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
