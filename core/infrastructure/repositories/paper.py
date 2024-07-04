from abc import ABC, abstractmethod
from typing import Optional
from core.domain.dto.paper import PaperDTO
from core.domain.paper import Paper


class PaperRepository(ABC):
    @abstractmethod
    def create_paper(self, paper: PaperDTO) -> Paper: ...

    @abstractmethod
    def get_papers(
        self,
        search: Optional[str],
        area: Optional[str],
        event_id: Optional[int],
        page: int = 1,
        page_size: int = 10,
        sort_by: str = 'title',
        sort_direction: str = 'asc' 
    ) -> list[Paper]: ...

    @abstractmethod
    def get_paper_by_id(self, paper_id: int) -> Paper: ...

    @abstractmethod
    def get_papers_by_area(self, area: str) -> list[Paper]: ...

    @abstractmethod
    def get_paper_by_pdf_id(self, pdf_id: str) -> Paper: ...

    @abstractmethod
    def get_first_paper(self) -> Paper: ...

    @abstractmethod
    def count_papers(
        self, search: Optional[str], area: Optional[str], event_id: Optional[int]
    ) -> int: ...

    @abstractmethod
    def count_papers_by_event_id(self, event_id: int) -> int: ...

    @abstractmethod
    def get_areas(self) -> list[str]: ...

    @abstractmethod
    def get_areas_by_event_id(self, event_id: int) -> list[str]: ...

    @abstractmethod
    def update_paper_pages(self, event_id: int, pdf_id: str, pages: int) -> Paper: ...
