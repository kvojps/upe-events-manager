from abc import ABC, abstractmethod
from pydantic import BaseModel


class UploadUrlResponse(BaseModel):
    url: str
    filename: str


class FileHandlerProvider(ABC):

    @abstractmethod
    def get_presigned_url(self) -> UploadUrlResponse | None: ...
