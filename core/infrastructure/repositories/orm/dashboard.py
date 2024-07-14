from core.infrastructure.repositories.dashboard import (
    DashboardRepository,
    DashboardData,
)
from core.infrastructure.settings.db_connection import get_session
from sqlalchemy import func
from core.domain.event import Event
from core.domain.subscriber import Subscriber
from core.domain.paper import Paper


class DashboardAdapter(DashboardRepository):
    def get_dashboard_data(self) -> DashboardData:
        with get_session() as session:
            total_subscribers = (
                session.query(func.count(Subscriber.id))
                .filter(Subscriber.is_present == False)
                .scalar(),
            )
            total_listeners = (
                session.query(func.count(Subscriber.id))
                .filter(Subscriber.is_present == True)
                .scalar(),
            )
            total_abseentes = total_subscribers[0] - total_listeners[0]

            return DashboardData(
                total_events=session.query(func.count(Event.id)).scalar(),
                total_papers=session.query(func.count(Paper.id)).scalar(),
                total_subscribers=total_subscribers[0],
                total_listeners=total_listeners[0],
                average_listeners_workload=session.query(func.avg(Subscriber.workload))
                .filter(Subscriber.is_present == True)
                .scalar(),
                papers_per_event=dict(
                    session.query(Event.name, func.count(Paper.id))
                    .join(Paper)
                    .group_by(Event.name)
                    .all()
                ),
                papers_per_area=dict(
                    session.query(Paper.area, func.count(Paper.id))
                    .group_by(Paper.area)
                    .all()
                ),
                participants_profile={
                    "subscribers": total_subscribers[0],
                    "listeners": total_listeners[0],
                    "abseentes": total_abseentes,
                },
            )
