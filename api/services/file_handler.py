from botocore.exceptions import ClientError
from fastapi import HTTPException, status
from pydantic import BaseModel
from api.ports.file_handler import FileHandlerProvider


class PutObjectResponse(BaseModel):
    key_filename: str


class FileHandlerService:
    def __init__(self, file_handler_repo: FileHandlerProvider):
        self._file_handler_repo = file_handler_repo

    def put_object(
        self, file_data: bytes, folder_name: str, file_name: str
    ) -> PutObjectResponse:
        key_filename = ""
        try:
            key_filename = self._file_handler_repo.put_object(
                file_data,
                folder_name,
                file_name,
            )
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
            )

        return PutObjectResponse(key_filename=key_filename)
