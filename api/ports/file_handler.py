from abc import ABC, abstractmethod


class FileHandlerProvider(ABC):
    @abstractmethod
    def put_object(self, file_to_upload: bytes, folder: str, key_obj: str) -> str: ...
