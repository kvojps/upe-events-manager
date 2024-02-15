from api.config.postgres import SessionLocal
from api.models.dto.paper import Paper as PaperDTO
from api.models.paper import Paper
from api.ports.paper import PaperRepository


class PaperAdapter(PaperRepository):
    def __init__(self):
        self._session = SessionLocal()

    def create_paper(self, paper: PaperDTO) -> Paper:
        paper_data = Paper(
            pdf_id=paper.pdf_id,
            pdf_filename=paper.pdf_filename,
            email=paper.email,
            title=paper.title,
            authors=paper.authors,
            isIgnored=paper.isIgnored,
            event_id=paper.event_id,
        )

        self._session.add(paper_data)
        self._session.commit()
        self._session.refresh(paper_data)

        return paper_data

    def get_papers(self) -> list[Paper]:
        return self._session.query(Paper).all()
