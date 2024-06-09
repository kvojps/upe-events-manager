from abc import ABC, abstractmethod


class FileHandlerProvider(ABC):
    @abstractmethod
    def download_object(self, key: str, download_file_path: str) -> None: ...

    @abstractmethod
    def put_object(self, file_to_upload: bytes, folder: str, key_obj: str) -> str: ...

    @abstractmethod
    def multipart_object_upload(
        self, file_to_upload: bytes, folder: str, key_obj: str
    ) -> str: ...
