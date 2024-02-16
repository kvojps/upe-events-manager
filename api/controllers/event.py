from fastapi import APIRouter, Depends, Query, status
from api.adapters.aws.file_handler import FileHandlerS3Adapter
from api.adapters.repository.event import EventAdapter
from api.adapters.repository.paper import PaperAdapter
from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.services.event import EventService, EventsPaginatedResponse
from api.services.file_handler import FileHandlerService, PutObjectResponse
from api.services.summary import SummaryService

router = APIRouter()

event_adapter = EventAdapter()
paper_adapter = PaperAdapter()
file_handler_adapter = FileHandlerS3Adapter()

service = EventService(event_adapter)
summary_service = SummaryService(paper_adapter, event_adapter)
file_handler_service = FileHandlerService(file_handler_adapter)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventDTO, event_service: EventService = Depends(lambda: service)
):
    return event_service.create_event(event_data)


@router.post(
    "/{event_id}/summary",
    response_model=PutObjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_summary(
    event_id: int,
    summary_service: SummaryService = Depends(lambda: summary_service),
    file_handler_service: FileHandlerService = Depends(lambda: file_handler_service),
    event_service: EventService = Depends(lambda: service),
):
    summary_pdf_response = summary_service.create_summary_pdf(event_id)
    file_handler_response = file_handler_service.put_object(
        summary_pdf_response.summary_pdf,
        summary_pdf_response.summary_pdf_folder,
        summary_pdf_response.summary_pdf_filename,
    )

    return file_handler_response


@router.get("", response_model=EventsPaginatedResponse, status_code=status.HTTP_200_OK)
def get_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    event_service: EventService = Depends(lambda: service),
):
    return event_service.get_events(page, page_size)
