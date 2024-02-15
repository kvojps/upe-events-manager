from abc import ABC, abstractmethod
from api.models.dto.paper import Paper as PaperDTO
from api.models.paper import Paper


class PaperRepository(ABC):
    @abstractmethod
    def create_paper(self, paper: PaperDTO) -> Paper: ...

    @abstractmethod
    def get_papers(self) -> list[Paper]: ...
