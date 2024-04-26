from fastapi import APIRouter, Depends, File, UploadFile, status
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
    page: int = 1,
    page_size: int = 10,
    subscriber_service: SubscriberService = Depends(lambda: service),
):
    return subscriber_service.get_subscribers_by_event_id(event_id, page, page_size)
