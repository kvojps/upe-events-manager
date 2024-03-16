from fastapi import APIRouter, Depends, File, Query, UploadFile, status, FastAPI, HTTPException
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
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

app = FastAPI()
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

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request, exc):
    if isinstance(exc.orig, UniqueViolation):
        error_message = "Um evento já cadastrado possui o mesmo nome"
        return JSONResponse(status_code=409, content={"error": error_message})
    else:
        raise HTTPException(status_code=500, detail="Internal Server Errror")

@router.post("", responses={409: {"description": "Conflito de valores", "model": integrity_error_handler}},
response_model=EventResponse)
def create_event(
    event_data: EventDTO, event_service: EventService = Depends(lambda: service)
):
    try:
        events = event_service.get_events()
        return event_service.create_event(event_data)
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            error_message = event_data.name + " já é um nome cadastrado."
            # Return a 409 HTTP response with a JSON payload containing the error message
            raise HTTPException(status_code=409, detail=error_message)
        else:
            # If it's not a unique violation, raise a generic HTTP exception
            raise HTTPException(status_code=500, detail="Internal server error")


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
