from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from api.adapters.aws.file_handler import FileHandlerS3Adapter
from api.adapters.repository.event import EventAdapter
from api.adapters.repository.paper import PaperAdapter
from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.services.anal import AnalService
from api.services.event import EventService, EventsPaginatedResponse
from api.services.file_handler import FileHandlerService
from api.services.merged_papers import MergedPapersService
from api.services.summary import SummaryService

router = APIRouter()

event_adapter = EventAdapter()
paper_adapter = PaperAdapter()
file_handler_adapter = FileHandlerS3Adapter()

service = EventService(event_adapter)
summary_service = SummaryService(paper_adapter, event_adapter)
file_handler_service = FileHandlerService(file_handler_adapter)

merged_papers_service = MergedPapersService(
    file_handler_service, event_adapter, paper_adapter
)

anal_service = AnalService(file_handler_service, event_adapter)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventDTO, event_service: EventService = Depends(lambda: service)
):
    return event_service.create_event(event_data)


@router.get("", response_model=EventsPaginatedResponse, status_code=status.HTTP_200_OK)
def get_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    event_service: EventService = Depends(lambda: service),
):
    return event_service.get_events(page, page_size)


@router.patch(
    "/{event_id}/summary",
    response_model=EventResponse,
    responses=
        {200: {"model": EventResponse}, 
         404: {"description": "Event not found"}},
    status_code=status.HTTP_200_OK,
)
def update_summary_filename(
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

    return event_service.update_summary_filename(
        event_id, file_handler_response.key_filename
    )


@router.patch(
    "/{event_id}/merged-papers",
    response_model=EventResponse,
    responses=
        {200: {"model": EventResponse},
         400: {"description": "Papers already merged for this event"},         
         404: {"description": "Event not found"},
         409: {"description": "Papers already created for this event"},
         415: {"description": "Unsupported Media Type"}, 
         500: {"description": "An error occurred while processing the file"}},
    status_code=status.HTTP_200_OK,
)
async def update_merged_papers_filename(
    event_id: int,
    file: UploadFile = File(...),
    merged_papers_service: MergedPapersService = Depends(lambda: merged_papers_service),
    event_service: EventService = Depends(lambda: service),
):
    merged_papers_response = await merged_papers_service.merge_pdf_files(event_id, file)

    return event_service.update_merged_papers_filename(
        event_id, merged_papers_response.key_filename
    )


@router.patch(
    "/{event_id}/anal",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
)
async def update_anal_filename(
    event_id: int,
    cover: UploadFile = File(...),
    anal_service: AnalService = Depends(lambda: anal_service),
    event_service: EventService = Depends(lambda: service),
):
    anal_pdf_response = await anal_service.create_anal_pdf(event_id, cover)

    return event_service.update_anal_filename(event_id, anal_pdf_response.key_filename)
