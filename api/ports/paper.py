from abc import ABC, abstractmethod
from api.models.paper import Paper


class PaperRepository(ABC):
    @abstractmethod
    def get_papers(self) -> list[Paper]: ...
