from api.contracts.responses.dashboard import DashboardDataResponse
from core.infrastructure.repositories.dashboard import DashboardRepository


class DashboardService:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    def get_dashboard_data(self) -> DashboardDataResponse:
        return DashboardDataResponse.from_domain(self.repository.get_dashboard_data())
