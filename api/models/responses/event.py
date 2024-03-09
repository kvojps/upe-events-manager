from typing import Optional
from pydantic import BaseModel
from api.config.dynaconf import settings
from api.models.event import Event


class EventResponse(BaseModel):
    id: int
    name: str
    initial_date: str
    final_date: str
    s3_folder_name: str
    summary_filename: Optional[str]
    merged_papers_filename: Optional[str]
    anal_filename: Optional[str]

    @classmethod
    def from_event(cls, event: Event) -> "EventResponse":
        return cls(
            id=int(event.id),
            name=str(event.name),
            initial_date=str(event.initial_date),
            final_date=str(event.final_date),
            s3_folder_name=str(event.s3_folder_name),
            summary_filename=(
                settings.CLOUDFRONT_DOMAIN + str(event.summary_filename)
                if event.summary_filename
                else None
            ),
            merged_papers_filename=(
                settings.CLOUDFRONT_DOMAIN + str(event.merged_papers_filename)
                if event.merged_papers_filename
                else None
            ),
            anal_filename=(
                settings.CLOUDFRONT_DOMAIN + str(event.anal_filename)
                if event.anal_filename
                else None
            ),
        )
