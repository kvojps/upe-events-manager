from abc import ABC, abstractmethod
from api.models.dto.paper import PaperDTO
from api.models.paper import Paper


class PaperRepository(ABC):
    @abstractmethod
    def create_paper(self, paper: PaperDTO) -> Paper: ...

    @abstractmethod
    def get_papers(self, page: int = 1, page_size: int = 10) -> list[Paper]: ...

    @abstractmethod
    def get_papers_by_area(self, area: str) -> list[Paper]: ...

    @abstractmethod
    def count_papers(self) -> int: ...

    @abstractmethod
    def count_papers_by_event_id(self, event_id: int) -> int: ...

    @abstractmethod
    def get_areas_by_event_id(self, event_id: int) -> list[str]: ...
