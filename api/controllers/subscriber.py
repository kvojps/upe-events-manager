from tempfile import NamedTemporaryFile
from fastapi import APIRouter, Depends, File, Query, UploadFile, status
from fastapi.responses import FileResponse
from api.contracts.responses.subscriber import BatchSubscribersResponse
from api.contracts.responses.subscriber import (
    SubscribersPaginatedResponse,
)
from core.application.subscriber import SubscriberService
from api.contracts.responses.exception import ExceptionResponse
from core.infrastructure.repositories.orm.event import EventAdapter
from core.infrastructure.repositories.orm.subscriber import SubscriberAdapter
from core.infrastructure.shared.cloud.aws.email_handler import EmailHandlerSESAdapter

router = APIRouter()

adapter = SubscriberAdapter()
event_adapter = EventAdapter()
ses_adapter = EmailHandlerSESAdapter()
service = SubscriberService(adapter, event_adapter, ses_adapter)


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


@router.post(
    "/{event_id}/send_certificates",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
    },
)
async def send_certificates(
    event_id: int,
    subscriber_service: SubscriberService = Depends(lambda: service),
):
    return await subscriber_service.send_all_certificates(event_id)
