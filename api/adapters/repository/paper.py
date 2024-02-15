from api.config.postgres import SessionLocal
from api.models.dto.paper import PaperDTO
from api.models.paper import Paper
from api.ports.paper import PaperRepository


class PaperAdapter(PaperRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_paper(self, paper: PaperDTO) -> Paper:
        paper_data = Paper(
            pdf_id=paper.pdf_id,
            title=paper.title,
            authors=paper.authors,
            isIgnored=paper.isIgnored,
            event_id=paper.event_id,
        )

        self._session.add(paper_data)
        self._session.commit()
        self._session.refresh(paper_data)

        return paper_data

    def get_papers(self, page: int = 1, page_size: int = 10) -> list[Paper]:
        papers = (
            self._session.query(Paper)
            .limit(page_size)
            .offset((page - 1) * page_size)
            .all()
        )

        return papers

    def count_papers(self) -> int:
        return self._session.query(Paper).count()

    def count_papers_by_event_id(self, event_id: int) -> int:
        return self._session.query(Paper).filter(Paper.event_id == event_id).count()
