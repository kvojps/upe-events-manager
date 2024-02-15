from api.models.dto.paper import PaperDTO
from api.models.responses.paper import PaperResponse
from api.ports.paper import PaperRepository


class PaperService:
    def __init__(self, paper_repo: PaperRepository):
        self._paper_repo = paper_repo

    def create_paper(self, paper: PaperDTO) -> PaperResponse:
        paper_data = self._paper_repo.create_paper(paper)

        return PaperResponse.from_paper(paper_data)

    def get_papers(self) -> list[PaperResponse]:
        papers_data = self._paper_repo.get_papers()

        return [PaperResponse.from_paper(paper_data) for paper_data in papers_data]
