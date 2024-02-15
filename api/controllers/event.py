from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import FileResponse
from api.adapters.repository.event import EventAdapter
from api.adapters.repository.paper import PaperAdapter
from api.models.dto.event import EventDTO
from api.models.responses.event import EventResponse
from api.services.event import EventService, EventsPaginatedResponse

router = APIRouter()

event_adapter = EventAdapter()
paper_adapter = PaperAdapter()
service = EventService(event_adapter, paper_adapter)


@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventDTO, event_service: EventService = Depends(lambda: service)
):
    return event_service.create_event(event_data)


@router.post(
    "/{event_id}/summary",
    status_code=status.HTTP_201_CREATED,
)
def create_summary(
    event_id: int, event_service: EventService = Depends(lambda: service)
):
    file_content = event_service.create_summary(event_id)
    with open("summary.pdf", "wb") as file:
        file.write(file_content)

    return FileResponse("summary.pdf", filename="summary.pdf")


@router.get("", response_model=EventsPaginatedResponse, status_code=status.HTTP_200_OK)
def get_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    event_service: EventService = Depends(lambda: service),
):
    return event_service.get_events(page, page_size)
