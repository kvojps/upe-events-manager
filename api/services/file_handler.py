from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from core.infrastructure.shared.cloud.file_handler import FileHandlerProvider
from api.services.responses.file_handler import PutObjectResponse


class FileHandlerService:
    def __init__(self, file_handler_repo: FileHandlerProvider):
        self._file_handler_repo = file_handler_repo

    def put_object(
        self, file_data: bytes, folder_name: str, file_name: str
    ) -> PutObjectResponse:
        key_filename = ""
        try:
            if len(file_data) < 25e6:
                key_filename = self._file_handler_repo.put_object(
                    file_data,
                    folder_name,
                    file_name,
                )
            else:
                key_filename = self._file_handler_repo.multipart_object_upload(
                    file_data,
                    folder_name,
                    file_name,
                )
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
            )

        return PutObjectResponse(key_filename=key_filename)

    def download_object(self, key: str, download_file_path: str) -> None:
        try:
            self._file_handler_repo.download_object(key, download_file_path)
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
            )
