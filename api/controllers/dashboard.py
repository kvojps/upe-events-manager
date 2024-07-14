from fastapi import APIRouter, Depends, status
from api.contracts.responses.dashboard import DashboardDataResponse
from api.contracts.responses.exception import ExceptionResponse
from core.application.dashboard import DashboardService
from core.infrastructure.repositories.orm.dashboard import DashboardAdapter

router = APIRouter()

adapter = DashboardAdapter()
service = DashboardService(adapter)


@router.get(
    "",
    response_model=DashboardDataResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
    },
)
def get_dashboard_data(service: DashboardService = Depends(lambda: service)):
    return service.get_dashboard_data()
