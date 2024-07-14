from pydantic import BaseModel
from core.infrastructure.repositories.dashboard import DashboardData


class DashboardDataResponse(BaseModel):
    total_events: int
    total_papers: int
    total_subscribers: int
    total_listeners: int
    average_listeners_workload: float
    papers_per_event: dict[str, int]
    papers_per_area: dict[str, int]
    participants_profile: dict[str, int]

    @classmethod
    def from_domain(cls, data: DashboardData) -> "DashboardDataResponse":
        return cls(**data.__dict__)
