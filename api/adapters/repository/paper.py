from api.config.postgres import SessionLocal
from api.models.paper import Paper
from api.ports.paper import PaperRepository


class PaperAdapter(PaperRepository):
    def __init__(self):
        self._session = SessionLocal()

    def get_papers(self) -> list[Paper]:
        return self._session.query(Paper).all()
