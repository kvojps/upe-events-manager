from abc import ABC, abstractmethod
from pydantic import BaseModel


class DashboardData(BaseModel):
    total_events: int
    total_papers: int
    total_subscribers: int
    total_listeners: int
    average_listeners_workload: float
    papers_per_event: dict[str, int]
    papers_per_area: dict[str, int]
    participants_profile: dict[str, int]


class DashboardRepository(ABC):
    @abstractmethod
    def get_dashboard_data(self) -> DashboardData: ...
