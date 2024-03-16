from typing import List, Optional
from api.models.dto.paper import PaperSchema
from api.models.paper import Paper
from fastapi import APIRouter, Depends, File, Query, UploadFile, status, HTTPException
from api.adapters.repository.event import EventAdapter
from api.adapters.repository.paper import PaperAdapter
from api.services.paper import PaperService, BatchPapersResponse, PapersPaginatedResponse

router = APIRouter()

paper_adapter = PaperAdapter()
event_adapter = EventAdapter()
paper_service = PaperService(paper_adapter, event_adapter)

@router.patch(
    "/upload_csv/events/{event_id}",
    response_model=list[BatchPapersResponse],
    status_code=status.HTTP_207_MULTI_STATUS,
)
async def batch_update_papers(
        event_id: int,
        file: UploadFile = File(...),
        paper_service: PaperService = Depends(lambda: paper_service),
):
    return await paper_service.batch_update_papers(event_id, file)

@router.get("", response_model=PapersPaginatedResponse, status_code=status.HTTP_200_OK)
def get_papers(
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100),
        paper_service: PaperService = Depends(lambda: paper_service),
):
    return paper_service.get_papers(page, page_size)

@router.get("/not_ignored", response_model=List[PaperSchema], status_code=status.HTTP_200_OK)
def get_not_ignored_papers(paper_service: PaperService = Depends(lambda: paper_service)):
    not_ignored_papers = paper_service.get_not_ignored_papers()
    if not not_ignored_papers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No papers found")
    return not_ignored_papers

@router.get("/papersFilter", response_model=List[PaperSchema], status_code=status.HTTP_200_OK)
def filter_papers_by_criteria(
        title: Optional[str] = None,
        author: Optional[str] = None,
        pdf_id: Optional[str] = None,
        area: Optional[str] = None,
        event_id: Optional[int] = None,
        paper_service: PaperService = Depends(lambda: paper_service),
):
    filtered_papers = paper_service.filter_papers_by_criteria(
        title=title, author=author, pdf_id=pdf_id, area=area, event_id=event_id
    )
    if not filtered_papers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No papers found")
    return filtered_papers
