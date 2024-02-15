from fastapi import APIRouter, Depends, status
from api.adapters.repository.paper import PaperAdapter
from api.models.dto.paper import PaperDTO
from api.models.responses.paper import PaperResponse
from api.services.paper import PaperService

router = APIRouter()

adapter = PaperAdapter()
service = PaperService(adapter)


@router.post("", response_model=PaperResponse, status_code=status.HTTP_201_CREATED)
def create_paper(
    paper_data: PaperDTO, paper_service: PaperService = Depends(lambda: service)
):
    return paper_service.create_paper(paper_data)


@router.get("", response_model=list[PaperResponse], status_code=status.HTTP_200_OK)
def get_paper(paper_service: PaperService = Depends(lambda: service)):
    return paper_service.get_papers()
