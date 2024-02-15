from botocore.exceptions import ClientError
from api.config.dynaconf import settings
from api.config.s3 import S3Config
from api.ports.file_handler import FileHandlerProvider


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._session = S3Config()
        self._bucket_name = settings.AWS_S3_BUCKET_NAME

    def put_object(self, file_to_upload: bytes, folder: str, key_obj: str):
        try:
            return self._session.s3_client.put_object(
                Body=file_to_upload,
                Bucket=self._bucket_name,
                Key=folder + "/" + key_obj,
            )
        except ClientError as e:
            raise RuntimeError(
                f"An error occurred while uploading {key_obj} to S3: {str(e)}"
            )
