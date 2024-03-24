from abc import ABC, abstractmethod
from typing import Optional
from api.models.dto.paper import PaperDTO, PaperToUpdateDTO
from api.models.paper import Paper


class PaperRepository(ABC):
    @abstractmethod
    def create_paper(self, paper: PaperDTO) -> Paper: ...

    @abstractmethod
    def get_papers(
        self,
        search: Optional[str],
        page: int = 1,
        page_size: int = 10,
    ) -> list[Paper]: ...

    @abstractmethod
    def get_papers_by_area(self, area: str) -> list[Paper]: ...

    @abstractmethod
    def get_paper_by_pdf_id(self, pdf_id: str) -> Paper: ...

    @abstractmethod
    def get_first_paper(self) -> Paper: ...

    @abstractmethod
    def count_papers(self, search: Optional[str]) -> int: ...

    @abstractmethod
    def count_papers_by_event_id(self, event_id: int) -> int: ...

    @abstractmethod
    def get_areas_by_event_id(self, event_id: int) -> list[str]: ...

    @abstractmethod
    def update_paper(self, pdf_id: int, paper: PaperToUpdateDTO) -> Paper: ...
