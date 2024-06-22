from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from core.domain.dto.event import EventDTO
from core.domain.dto.summary import SummaryDTO
from core.application.proceedings import ProceedingsService
from core.application.event import EventService
from core.application.file_handler import FileHandlerService
from core.application.merged_papers import MergedPapersService
from api.contracts.responses.event import EventResponse, EventsPaginatedResponse
from core.application.summary import SummaryService
from api.utils.doc_responses import ExceptionResponse
from core.infrastructure.repositories.orm.event import EventAdapter
from core.infrastructure.repositories.orm.paper import PaperAdapter
from core.infrastructure.shared.cloud.aws.file_handler import FileHandlerS3Adapter

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
anal_service = ProceedingsService(file_handler_service, event_adapter)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ExceptionResponse},
    },
)
def create_event(
    event_data: EventDTO, event_service: EventService = Depends(lambda: service)
):
    return event_service.create_event(event_data)


@router.get("", response_model=EventsPaginatedResponse, status_code=status.HTTP_200_OK)
def get_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    initial_date: str = Query(None),
    final_date: str = Query(None),
    name: str = Query(None),
    event_service: EventService = Depends(lambda: service),
):
    return event_service.get_events(initial_date, final_date, name, page, page_size)


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ExceptionResponse}},
)
def get_event_by_id(
    event_id: int, event_service: EventService = Depends(lambda: service)
):
    return event_service.get_event_by_id(event_id)


@router.patch(
    "/{event_id}/summary",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ExceptionResponse},
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        503: {"model": ExceptionResponse},
    },
)
def update_summary_filename(
    event_id: int,
    summmary_dto: SummaryDTO,
    summary_service: SummaryService = Depends(lambda: summary_service),
    file_handler_service: FileHandlerService = Depends(lambda: file_handler_service),
    event_service: EventService = Depends(lambda: service),
):
    summary_pdf_response = summary_service.create_summary_pdf(event_id, summmary_dto)
    file_handler_response = file_handler_service.put_object(
        summary_pdf_response.summary_pdf,
        summary_pdf_response.summary_pdf_folder,
        summary_pdf_response.summary_pdf_filename,
    )

    return event_service.update_summary_filename(
        event_id, file_handler_response.key_filename
    )


@router.patch(
    "/{event_id}/merged_papers",
    response_model=EventResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ExceptionResponse},
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        409: {"model": ExceptionResponse},
        415: {"model": ExceptionResponse},
        500: {"model": ExceptionResponse},
    },
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
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        415: {"model": ExceptionResponse},
        503: {"model": ExceptionResponse},
    },
)
async def update_anal_filename(
    event_id: int,
    cover: UploadFile = File(...),
    anal_service: ProceedingsService = Depends(lambda: anal_service),
    event_service: EventService = Depends(lambda: service),
):
    anal_pdf_response = await anal_service.create_anal_pdf(event_id, cover)

    return event_service.update_anal_filename(event_id, anal_pdf_response.key_filename)
