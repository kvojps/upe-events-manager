from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from api.adapters.repository.event import EventAdapter
from api.adapters.repository.paper import PaperAdapter
from api.services.paper import (
    BatchPapersResponse,
    PaperService,
    PapersPaginatedResponse,
    AreasResponse,
)
from api.utils.doc_responses import ExceptionResponse

router = APIRouter()

adapter = PaperAdapter()
event_adapter = EventAdapter()
service = PaperService(adapter, event_adapter)


@router.patch(
    "/upload_csv/events/{event_id}",
    response_model=BatchPapersResponse,
    status_code=status.HTTP_207_MULTI_STATUS,
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        415: {"model": ExceptionResponse},
    },
)
async def batch_update_papers(
    event_id: int,
    file: UploadFile = File(...),
    paper_service: PaperService = Depends(lambda: service),
):
    return await paper_service.batch_update_papers(event_id, file)


@router.get("", response_model=PapersPaginatedResponse, status_code=status.HTTP_200_OK)
def get_papers(
    search: str = Query(None),
    area: str = Query(None),
    event_id: int = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    paper_service: PaperService = Depends(lambda: service),
):
    return paper_service.get_papers(search, area, event_id, page, page_size)


@router.get("/areas", response_model=AreasResponse, status_code=status.HTTP_200_OK)
def get_areas(paper_service: PaperService = Depends(lambda: service)):
    return paper_service.get_areas()
