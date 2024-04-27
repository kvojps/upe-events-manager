from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import FileResponse
from api.adapters.repository.event import EventAdapter
from api.adapters.repository.subscriber import SubscriberAdapter
from api.services.responses.subscriber import (
    BatchSubscribersResponse,
    SubscribersPaginatedResponse,
)
from api.services.subscriber import SubscriberService
from api.utils.doc_responses import ExceptionResponse

router = APIRouter()

adapter = SubscriberAdapter()
event_adapter = EventAdapter()
service = SubscriberService(adapter, event_adapter)


@router.post(
    "/{event_id}",
    response_model=BatchSubscribersResponse,
    status_code=status.HTTP_207_MULTI_STATUS,
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        415: {"model": ExceptionResponse},
    },
)
async def batch_create_subscribers(
    event_id: int,
    file: UploadFile = File(...),
    subscriber_service: SubscriberService = Depends(lambda: service),
):
    return await subscriber_service.batch_create_subscribers(event_id, file)


@router.get(
    "/{event_id}",
    response_model=SubscribersPaginatedResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
    },
)
def get_subscribers(
    event_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    subscriber_service: SubscriberService = Depends(lambda: service),
):
    return subscriber_service.get_subscribers_by_event_id(event_id, page, page_size)


@router.get(
    "/{event_id}/certificate",
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
    },
)
async def get_subscriber_certificate(
    event_id: int,
    email: str,
    subscriber_service: SubscriberService = Depends(lambda: service),
):
    file_bytes = subscriber_service.get_subscriber_certificate(event_id, email)

    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_bytes)
        temp_file.seek(0)

        return FileResponse(
            temp_file.name,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={email}_certificate.pdf"
            },
        )


@router.patch(
    "/{event_id}",
    response_model=BatchSubscribersResponse,
    status_code=status.HTTP_207_MULTI_STATUS,
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        415: {"model": ExceptionResponse},
    },
)
async def update_subscribers(
    event_id: int,
    file: UploadFile = File(...),
    subscriber_service: SubscriberService = Depends(lambda: service),
):
    return await subscriber_service.batch_update_subscribers(event_id, file)
