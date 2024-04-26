from pydantic import BaseModel
from api.models.subscriber import Subscriber


class SubscriberResponse(BaseModel):
    id: int
    name: str
    cpf: str
    email: str
    workload: str
    is_present: bool
    event_id: int

    @classmethod
    def from_subscriber(cls, subscriber: Subscriber) -> "SubscriberResponse":
        return cls(
            id=int(subscriber.id),
            name=str(subscriber.name),
            cpf=str(subscriber.cpf),
            email=str(subscriber.email),
            workload=str(subscriber.workload),
            is_present=bool(subscriber.is_present),
            event_id=int(subscriber.event_id),
        )


class BatchSubscribersErrorResponse(BaseModel):
    id: str
    message: str


class BatchSubscribersResponse(BaseModel):
    detail: str
    errors: list[BatchSubscribersErrorResponse]


class SubscribersPaginatedResponse(BaseModel):
    subscribers: list[SubscriberResponse]
    total_subscribers: int
    total_pages: int
    current_page: int

    @classmethod
    def from_subscribers(
        cls,
        subscribers: list[Subscriber],
        total_subscribers: int,
        total_pages: int,
        current_page: int,
    ) -> "SubscribersPaginatedResponse":
        return cls(
            subscribers=[
                SubscriberResponse.from_subscriber(subscriber)
                for subscriber in subscribers
            ],
            total_subscribers=total_subscribers,
            total_pages=total_pages,
            current_page=current_page,
        )
