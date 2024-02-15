from api.ports.paper import PaperRepository
from api.models.dto.paper import Paper as PaperDTO
from api.models.responses.paper import PaperResponse


class PaperService:
    def __init__(self, paper_repo: PaperRepository):
        self._paper_repo = paper_repo

    def create_paper(self, paper: PaperDTO) -> PaperResponse:
        paper_data = self._paper_repo.create_paper(paper)

        return paper_data

    def get_papers(self) -> list[PaperResponse]:
        papers_data = self._paper_repo.get_papers()

        return [
            PaperResponse(
                pdf_id=str(paper.pdf_id),
                pdf_filename=str(paper.pdf_filename),
                email=str(paper.email),
                title=str(paper.title),
                authors=str(paper.authors),
                isIgnored=bool(paper.isIgnored),
                event_id=int(paper.event_id),
            )
            for paper in papers_data
        ]
