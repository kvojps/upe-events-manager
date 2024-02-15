import uuid
from botocore.exceptions import ClientError
from fastapi import HTTPException
from api.config.dynaconf import settings
from api.config.s3 import S3Config
from api.ports.file_handler import FileHandlerProvider, UploadUrlResponse


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._session = S3Config()
        self._bucket_name = settings.AWS_S3_BUCKET_NAME

    def get_presigned_url(self) -> UploadUrlResponse | None:
        try:
            key_obj = f"{str(uuid.uuid4())}.docx"
            url = self._session.s3_client.generate_presigned_url(
                "put_object",
                Params={"Bucket": self._bucket_name, "Key": key_obj},
                ExpiresIn=3600,
            )

            return UploadUrlResponse(url=url, filename=key_obj)

        except ClientError as e:
            error_status_code = e.response["ResponseMetadata"]["HTTPStatusCode"]
            error_message = e.response["message"]  # type: ignore

            raise HTTPException(status_code=error_status_code, detail=error_message)
